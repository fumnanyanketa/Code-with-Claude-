#!/usr/bin/env python3
"""Extract transcripts for every video in the two Code with Claude playlists.

YouTube bot-detection on cloud IPs is probabilistic, so this script rotates
player clients, retries with backoff, throttles between videos, and resumes
(skipping videos whose transcript file already exists).
"""
import os, re, ssl, json, time, random, urllib.request

CA = "/etc/ssl/certs/ca-certificates.crt"

# Make yt-dlp's bundled certifi trust the proxy CA without modifying any file.
import certifi
certifi.where = lambda: CA
import yt_dlp

SSL_CTX = ssl.create_default_context(cafile=CA)
OUT_ROOT = "transcripts"
# `tv`/`tv_embedded` return downloadable captions without a PO token. Keeping the
# request volume low (few clients, long gaps) is what keeps the cloud IP from being
# flagged; the node JS runtime solves YouTube's bot-detection JS challenge.
CLIENTS = ["tv", "tv_embedded", "mweb", "web_safari"]
NODE = "/opt/node22/bin/node"
COOKIES = "cookies.txt"  # authenticated session -> bypasses cloud-IP bot detection
YDL_BASE = {
    "quiet": True, "skip_download": True, "no_warnings": True,
}
if os.path.exists(COOKIES):
    # Cookies alone defeat the bot check and are ~15x faster than running the
    # JS-challenge solver on every request.
    YDL_BASE["cookiefile"] = COOKIES
else:
    # No cookies: fall back to yt-dlp's EJS solver via Node to beat bot detection.
    YDL_BASE["js_runtimes"] = {"node": {"path": NODE}}
    YDL_BASE["remote_components"] = ["ejs:github"]

def slugify(title, vid):
    if not title:
        return vid
    s = re.sub(r"[^\w\s-]", "", title).strip().lower()
    s = re.sub(r"[\s_-]+", "-", s)
    return (s[:70].strip("-")) or vid

class NoCaptions(Exception):
    """Video extracted fine but YouTube has no English caption track for it.
    (Permanent — only audio transcription via Whisper could produce a transcript.)"""

def get_transcript(vid):
    """Rotate clients. For each client that returns a caption track, actually
    download+parse it; only accept a client whose caption URL yields real text.
    Returns (real_title, lang, kind, client, plain, lines)."""
    last_err = "no working client"
    got_response = False  # at least one client returned a player response
    real_title = vid
    for client in CLIENTS:
        opts = dict(YDL_BASE)
        opts["extractor_args"] = {"youtube": {"player_client": [client]}}
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(
                    f"https://www.youtube.com/watch?v={vid}",
                    download=False, process=False)
        except Exception as e:
            last_err = str(e).splitlines()[0]
            time.sleep(random.uniform(2, 4))
            continue
        got_response = True
        real_title = info.get("title") or real_title
        track, lang, kind = pick_track(info)
        if not track:
            last_err = "no english caption track"
            time.sleep(random.uniform(2, 4))
            continue
        try:
            plain, lines = fetch_caption_text(track)
            if plain:
                return real_title, lang, kind, client, plain, lines
            last_err = "empty transcript body"
        except Exception as e:
            last_err = str(e).splitlines()[0]
        time.sleep(random.uniform(2, 4))
    # Distinguish "no captions exist" (don't bother cooling down / retrying) from
    # an actual block where every client request errored out.
    if got_response and last_err == "no english caption track":
        raise NoCaptions(real_title)
    raise RuntimeError(last_err)

def pick_track(info):
    subs = info.get("subtitles") or {}
    autos = info.get("automatic_captions") or {}
    def find(d):
        for key in ("en", "en-US", "en-GB", "en-orig"):
            if key in d:
                return d[key], key
        for k in d:
            if k.startswith("en"):
                return d[k], k
        return None, None
    track, lang = find(subs)
    if track:
        return track, lang, "manual"
    track, lang = find(autos)
    if track:
        return track, lang, "auto"
    return None, None, None

def _http_get(url):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            return urllib.request.urlopen(req, context=SSL_CTX, timeout=60).read()
        except Exception:
            time.sleep(2 ** attempt)
    return None

def fetch_caption_text(track):
    """Return (plain_text, timestamped_lines). Try json3, then srv3/ttml/vtt."""
    # Prefer json3, but the URL can intermittently return an empty/non-JSON body,
    # so fall back across the other available caption formats.
    ordered = sorted(track, key=lambda f: 0 if f.get("ext") == "json3" else 1)
    for f in ordered:
        raw = _http_get(f["url"])
        if not raw or not raw.strip():
            continue
        ext = f.get("ext")
        try:
            if ext == "json3":
                return parse_json3(raw)
            if ext in ("vtt", "srv3", "srv2", "srv1", "ttml", "srt"):
                return parse_vtt_like(raw, ext)
        except Exception:
            continue
    raise RuntimeError("caption download/parse failed (empty body)")

def parse_vtt_like(raw, ext):
    """Crude parser for vtt/ttml/srv* -> (plain, timestamped lines)."""
    text = raw.decode("utf-8", "replace")
    # Strip tags, cue settings, and indices; keep text + first timestamp per cue.
    text = re.sub(r"<[^>]+>", " ", text)
    plain_parts, lines = [], []
    for block in re.split(r"\n\s*\n", text):
        ts = None
        m = re.search(r"(\d{1,2}:\d{2}:\d{2})[.,]\d+", block)
        if m:
            ts = m.group(1)
        body = []
        for ln in block.splitlines():
            ln = ln.strip()
            if not ln or "-->" in ln or ln.upper() in ("WEBVTT",) or ln.isdigit():
                continue
            if re.match(r"^(Kind|Language|NOTE)", ln):
                continue
            body.append(ln)
        seg = " ".join(body).strip()
        if seg:
            plain_parts.append(seg)
            if ts:
                lines.append(f"[{ts}] {seg}")
            else:
                lines.append(seg)
    plain = re.sub(r"\s+", " ", " ".join(plain_parts)).strip()
    return plain, lines

def parse_json3(raw):
    """Return (plain_text, timestamped_lines)."""
    doc = json.loads(raw)
    plain_parts, lines = [], []
    for ev in doc.get("events", []):
        segs = ev.get("segs") or []
        text = "".join(s.get("utf8", "") for s in segs)
        text = text.replace("\n", " ").strip()
        if not text:
            continue
        plain_parts.append(text)
        start_ms = ev.get("tStartMs", 0)
        t = int(start_ms // 1000)
        ts = f"{t//3600:02d}:{(t%3600)//60:02d}:{t%60:02d}"
        lines.append(f"[{ts}] {text}")
    # Collapse into readable paragraphs.
    plain = " ".join(plain_parts)
    plain = re.sub(r"\s+", " ", plain).strip()
    return plain, lines

def wrap(text, width=100):
    out, line = [], ""
    for word in text.split():
        if len(line) + len(word) + 1 > width:
            out.append(line)
            line = word
        else:
            line = (line + " " + word).strip()
    if line:
        out.append(line)
    return "\n".join(out)

def process_one(pkey, pl, pdir, idx, v):
    vid, title = v["id"], v.get("title")
    base = f"{idx:02d}_{slugify(title, vid)}"
    txt_path = os.path.join(pdir, base + ".txt")
    ts_path = os.path.join(pdir, base + ".timestamped.txt")
    nocap_path = os.path.join(pdir, base + ".nocaptions")
    if os.path.exists(txt_path) and os.path.getsize(txt_path) > 0:
        return "done"
    if os.path.exists(nocap_path):
        return "nocaps"  # known: no captions on YouTube, needs Whisper
    if os.path.exists(os.path.join(pdir, base + ".unavailable")):
        return "gone"  # known: removed/private on YouTube
    try:
        real_title, lang, kind, client, plain, lines = get_transcript(vid)
        real_title = real_title or title or vid
        header = (f"Title: {real_title}\nVideo: https://www.youtube.com/watch?v={vid}\n"
                  f"Caption: {kind} ({lang}) via {client}\n"
                  f"{'='*80}\n\n")
        with open(txt_path, "w") as f:
            f.write(header + wrap(plain) + "\n")
        with open(ts_path, "w") as f:
            f.write(header + "\n".join(lines) + "\n")
        print(f"[ OK ] {pkey} {idx:02d} {vid} {len(plain):>7d} chars  {kind}/{lang}  {real_title[:50]}", flush=True)
        return "ok"
    except NoCaptions as e:
        with open(nocap_path, "w") as f:
            f.write(f"{e}\nhttps://www.youtube.com/watch?v={vid}\n")
        print(f"[NOCAP] {pkey} {idx:02d} {vid}  no YouTube captions (needs Whisper)", flush=True)
        return "nocaps"
    except Exception as e:
        msg = str(e).splitlines()[0][:120]
        if re.search(r"unavailable|removed by the uploader|private video|been terminated", msg, re.I):
            with open(os.path.join(pdir, base + ".unavailable"), "w") as f:
                f.write(f"{msg}\nhttps://www.youtube.com/watch?v={vid}\n")
            print(f"[GONE ] {pkey} {idx:02d} {vid}  video unavailable/removed", flush=True)
            return "gone"
        print(f"[FAIL] {pkey} {idx:02d} {vid}  {msg}", flush=True)
        return "fail"

def main():
    data = json.load(open("playlists.json"))
    MAX_PASSES = 12
    streak = 0  # consecutive failures -> adaptive cooldown to clear IP rate-limit
    for p in range(1, MAX_PASSES + 1):
        remaining = 0
        progressed = 0
        print(f"\n----- PASS {p} -----", flush=True)
        for pkey, pl in data.items():
            pdir = os.path.join(OUT_ROOT, slugify(pl["title"], pkey))
            os.makedirs(pdir, exist_ok=True)
            for idx, v in enumerate(pl["videos"], 1):
                r = process_one(pkey, pl, pdir, idx, v)
                if r in ("done", "nocaps", "gone"):
                    # Already have it, or it permanently can't be fetched (no captions
                    # / removed): no retry, no cooldown (not rate-limit failures).
                    if r in ("nocaps", "gone"):
                        streak = 0
                        time.sleep(random.uniform(1, 3))
                    continue
                # With cookies the IP is rarely blocked, so keep pacing light; only
                # back off if real failures actually streak (transient rate-limit).
                if r == "ok":
                    progressed += 1
                    streak = 0
                    time.sleep(random.uniform(2, 5))
                else:  # fail
                    remaining += 1
                    streak += 1
                    if streak >= 3:
                        cool = min(60 + 30 * (streak - 2), 240)
                        print(f"   ...cooldown {cool:.0f}s after {streak} fail(s)", flush=True)
                        time.sleep(cool + random.uniform(0, 15))
                    else:
                        time.sleep(random.uniform(3, 7))
        print(f"----- PASS {p} done: {progressed} new, {remaining} still failing -----", flush=True)
        if remaining == 0:
            break
        if progressed == 0:
            time.sleep(random.uniform(120, 240))  # whole pass stuck: long cooldown

    # Final summary
    summary = []
    for pkey, pl in data.items():
        pdir = os.path.join(OUT_ROOT, slugify(pl["title"], pkey))
        for idx, v in enumerate(pl["videos"], 1):
            base = f"{idx:02d}_{slugify(v.get('title'), v['id'])}"
            txt_path = os.path.join(pdir, base + ".txt")
            nocap_path = os.path.join(pdir, base + ".nocaptions")
            if os.path.exists(txt_path) and os.path.getsize(txt_path) > 0:
                status = "ok"
            elif os.path.exists(nocap_path):
                status = "no_captions"
            elif os.path.exists(os.path.join(pdir, base + ".unavailable")):
                status = "unavailable"
            else:
                status = "missing"
            summary.append({"playlist": pkey, "n": idx, "id": v["id"],
                            "title": v.get("title"), "status": status})
    json.dump(summary, open("extract_summary.json", "w"), indent=2)
    ok = sum(1 for s in summary if s["status"] == "ok")
    nocap = sum(1 for s in summary if s["status"] == "no_captions")
    gone = sum(1 for s in summary if s["status"] == "unavailable")
    print(f"\nDONE: {ok}/{len(summary)} transcripts available "
          f"({nocap} have no YouTube captions / need Whisper, {gone} removed from YouTube)", flush=True)
    for s in summary:
        if s["status"] != "ok":
            print(f"  {s['status'].upper()}: {s['playlist']} {s['n']:02d} {s['id']} {s['title']}", flush=True)

if __name__ == "__main__":
    main()
