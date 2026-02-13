import os
import shutil
import yt_dlp
from yt_dlp.utils import match_filter_func
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment


# -------------------------
# Clean previous run folders
# -------------------------
def clean_dirs():
    for d in ["videos", "audios", "trimmed"]:
        if os.path.exists(d):
            shutil.rmtree(d)


# -------------------------
# Main mashup function
# -------------------------
def run_mashup(singer, num_videos, duration, output_file):

    print("\n🎵 Starting mashup process...")

    clean_dirs()

    os.makedirs("videos", exist_ok=True)
    os.makedirs("audios", exist_ok=True)
    os.makedirs("trimmed", exist_ok=True)

    # -------------------------
    # Step 1 — Download videos
    # -------------------------
    query = f"ytsearch{num_videos}:{singer} song"

    ydl_opts = {
        "format": "mp4",
        "outtmpl": "videos/%(title)s.%(ext)s",
        "quiet": False,

        # robustness
        "retries": 5,
        "fragment_retries": 5,
        "ignoreerrors": True,
        "nocheckcertificate": True,

        # skip long videos (>10 min)
        "match_filter": match_filter_func("duration < 600"),
    }

    print("⬇️ Downloading short song videos only...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([query])

    print("✅ Download phase complete")

    # -------------------------
    # Step 2 — Extract audio
    # -------------------------
    print("🎧 Extracting audio...")

    video_files = [f for f in os.listdir("videos") if f.endswith(".mp4")]

    if not video_files:
        raise RuntimeError("❌ No valid videos downloaded")

    for file in video_files:
        vpath = os.path.join("videos", file)
        apath = os.path.join("audios", file[:-4] + ".mp3")

        print(f"🎵 Processing: {file}")

        try:
            clip = VideoFileClip(vpath)

            if clip.audio is None:
                print("⚠️ No audio stream — skipped")
                clip.close()
                continue

            clip.audio.write_audiofile(apath)
            clip.close()

            print(f"✅ Extracted → {apath}")

        except Exception as e:
            print(f"⚠️ Failed extract → {file} : {e}")

    print("✅ Audio extraction complete")

    # -------------------------
    # Step 3 — Trim clips
    # -------------------------
    print("✂️ Trimming clips...")

    audio_files = [f for f in os.listdir("audios") if f.endswith(".mp3")]

    if not audio_files:
        raise RuntimeError("❌ No audio clips available")

    for file in audio_files:
        try:
            path = os.path.join("audios", file)
            audio = AudioSegment.from_mp3(path)

            trimmed = audio[:duration * 1000]
            trimmed.export(os.path.join("trimmed", file), format="mp3")

            print(f"✂️ Trimmed → {file}")

        except Exception as e:
            print(f"⚠️ Trim failed → {file} : {e}")

    print("✅ Trimming complete")

    # -------------------------
    # Step 4 — Merge
    # -------------------------
    print("🔗 Merging clips...")

    trimmed_files = [f for f in os.listdir("trimmed") if f.endswith(".mp3")]

    if not trimmed_files:
        raise RuntimeError("❌ No trimmed clips available")

    final = AudioSegment.empty()

    for file in trimmed_files:
        try:
            final += AudioSegment.from_mp3(os.path.join("trimmed", file))
            print(f"➕ Added → {file}")
        except Exception as e:
            print(f"⚠️ Merge skip → {file} : {e}")

    final.export(output_file, format="mp3")

    print(f"\n🎉 Mashup created successfully → {output_file}")
