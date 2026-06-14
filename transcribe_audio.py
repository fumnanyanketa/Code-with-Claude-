#!/usr/bin/env python3
"""Transcribe the talks that have no YouTube captions, using Groq Whisper.

For each video marked `*.nocaptions`, download its audio with yt-dlp, split it
into small chunks with ffmpeg, send each chunk to Groq's whisper-large-v3, and
assemble a transcript in the same format as the caption-based ones.

Needs GROQ_API_KEY (env var, or a KEY=VALUE line in a local .env file).
Resumable: skips talks whose transcript already exists.
"""
import os, re, ssl, json, time, glob, tempfile, subprocess

CA = "/etc/ssl/certs/ca-certificates.crt"
import certifi
certifi.where = lambda: CA
import yt_dlp
import imageio_ffmpeg
from groq import Groq

OUT_ROOT = "transcripts"
COOKIES = "cookies.txt"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
CHUNK_SECONDS = 600           # ~10 min per chunk -> small files, safe under limits
GROQ_MODEL = "whisper-large-v3"

def load_env():
    if os.environ.get("GROQ_API_KEY"):
        return os.environ["GROQ_API_KEY"]
    if os.path.exists(".env"):
        for line in open(".env"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                if k.strip() == "GROQ_API_KEY":
                    return v.strip().strip('"').strip("'")
    raise SystemExit("GROQ_API_KEY not set (env or .env)")

def slugify(title, vid):
    if not title:
        return vid
    s = re.sub(r"[^\w\s-]", "", title).strip().lower()
    s = re.sub(r"[\s_-]+", "-", s)
    return (s[:70].strip("-")) or vid

def download_audio(vid, dest_dir):
    """Download bestaudio (no ffmpeg post-processing) -> path to the raw file."""
    opts = {
        "quiet": True, "no_warnings": True,
        "format": "bestaudio/best",
        "outtmpl": os.path.join(dest_dir, "%(id)s.%(ext)s"),
    }
    if os.path.exists(COOKIES):
        opts["cookiefile"] = COOKIES
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={vid}", download=True)
    files = glob.glob(os.path.join(dest_dir, f"{vid}.*"))
    if not files:
        raise RuntimeError("audio download produced no file")
    return files[0], info.get("title") or vid

def split_audio(src, dest_dir):
    """Re-encode to 16 kHz mono mp3 and segment into CHUNK_SECONDS pieces."""
    pattern = os.path.join(dest_dir, "chunk_%04d.mp3")
    cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-i", src,
           "-ac", "1", "-ar", "16000", "-b:a", "64k",
           "-f", "segment", "-segment_time", str(CHUNK_SECONDS), pattern]
    subprocess.run(cmd, check=True)
    return sorted(glob.glob(os.path.join(dest_dir, "chunk_*.mp3")))

def transcribe_chunks(client, chunks):
    """Return (plain_text, timestamped_lines) across all chunks."""
    plain_parts, lines = [], []
    for i, chunk in enumerate(chunks):
        offset = i * CHUNK_SECONDS
        for attempt in range(4):
            try:
                with open(chunk, "rb") as f:
                    resp = client.audio.transcriptions.create(
                        file=(os.path.basename(chunk), f.read()),
                        model=GROQ_MODEL,
                        response_format="verbose_json",
                        language="en",
                    )
                break
            except Exception as e:
                if attempt == 3:
                    raise
                time.sleep(2 ** attempt)
        segments = getattr(resp, "segments", None) or []
        if segments:
            for seg in segments:
                text = (seg.get("text") if isinstance(seg, dict) else seg.text).strip()
                start = (seg.get("start") if isinstance(seg, dict) else seg.start) or 0
                if not text:
                    continue
                t = int(offset + start)
                ts = f"{t//3600:02d}:{(t%3600)//60:02d}:{t%60:02d}"
                plain_parts.append(text)
                lines.append(f"[{ts}] {text}")
        else:
            text = (resp.text or "").strip()
            if text:
                plain_parts.append(text)
                t = int(offset)
                lines.append(f"[{t//3600:02d}:{(t%3600)//60:02d}:{t%60:02d}] {text}")
    plain = re.sub(r"\s+", " ", " ".join(plain_parts)).strip()
    return plain, lines

def wrap(text, width=100):
    out, line = [], ""
    for word in text.split():
        if len(line) + len(word) + 1 > width:
            out.append(line); line = word
        else:
            line = (line + " " + word).strip()
    if line:
        out.append(line)
    return "\n".join(out)

def main():
    client = Groq(api_key=load_env())
    data = json.load(open("playlists.json"))
    done = fail = 0
    for pkey, pl in data.items():
        pdir = os.path.join(OUT_ROOT, slugify(pl["title"], pkey))
        for idx, v in enumerate(pl["videos"], 1):
            vid = v["id"]
            base = f"{idx:02d}_{slugify(v.get('title'), vid)}"
            txt_path = os.path.join(pdir, base + ".txt")
            nocap_path = os.path.join(pdir, base + ".nocaptions")
            if not os.path.exists(nocap_path):
                continue  # only the caption-less talks
            if os.path.exists(txt_path) and os.path.getsize(txt_path) > 0:
                continue
            try:
                with tempfile.TemporaryDirectory() as tmp:
                    audio, real_title = download_audio(vid, tmp)
                    chunks = split_audio(audio, tmp)
                    plain, lines = transcribe_chunks(client, chunks)
                if not plain:
                    raise RuntimeError("empty transcription")
                header = (f"Title: {real_title}\nVideo: https://www.youtube.com/watch?v={vid}\n"
                          f"Caption: whisper ({GROQ_MODEL}, audio transcription)\n"
                          f"{'='*80}\n\n")
                with open(txt_path, "w") as f:
                    f.write(header + wrap(plain) + "\n")
                with open(os.path.join(pdir, base + ".timestamped.txt"), "w") as f:
                    f.write(header + "\n".join(lines) + "\n")
                os.remove(nocap_path)
                done += 1
                print(f"[ OK ] {pkey} {idx:02d} {vid} {len(plain):>7d} chars  {real_title[:50]}", flush=True)
            except Exception as e:
                fail += 1
                print(f"[FAIL] {pkey} {idx:02d} {vid}  {str(e).splitlines()[0][:110]}", flush=True)
            time.sleep(1)
    print(f"\nDONE: {done} transcribed, {fail} failed", flush=True)

if __name__ == "__main__":
    main()
