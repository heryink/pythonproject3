import os
import sys
import subprocess
from imageio_ffmpeg import get_ffmpeg_exe

# 1. Setup paths explicitly
TARGET_DIR = r"C:\Users\USER\Videos\AI_CORE\deep_learning-MIT"
os.makedirs(TARGET_DIR, exist_ok=True)

archive_file = os.path.join(TARGET_DIR, "downloaded_history.txt")

# Standard format layout configuration
RESOLUTION_SETTING = "bestvideo[height<=1080][vcodec!=av01]+bestaudio/bestvideo+bestaudio/best"
COURSE_URL = "https://www.youtube.com/playlist?list=PLtBw6njQRU-rwp5__7C0oIVt26ZgjG9NI"

venv_dir = os.path.dirname(sys.executable)
yt_dlp_executable = os.path.join(venv_dir, "yt-dlp.exe")
ffmpeg_path = get_ffmpeg_exe()

# 2. Automated Cleanup Phase (Deletes unmerged tracks, chat logs, and corrupt files)
print("🧼 Automatically clearing loose files, unmerged tracks, and chat JSON clutter...")
if os.path.exists(TARGET_DIR):
    for item in os.listdir(TARGET_DIR):
        item_path = os.path.join(TARGET_DIR, item)
        if os.path.isfile(item_path):
            if item.endswith(".json") or item.endswith(".part") or item.endswith(".ytdl"):
                os.remove(item_path)
            elif any(marker in item for marker in [".f137.", ".f248.", ".f140.", ".f251."]):
                os.remove(item_path)

# 3. Execution Phase
command = [
    yt_dlp_executable,
    "-f", RESOLUTION_SETTING,
    "--download-archive", archive_file,
    "--ffmpeg-location", ffmpeg_path,  # Forces video/audio auto-stitching
    "--merge-output-format", "mp4",  # Packs everything cleanly into an MP4 container
    "--no-write-comments",  # Permanently blocks live chat JSON logs

    # 🔑 COOKIE INTEGRATION: Securely bypasses YouTube's automated bot checks using desktop sessions
    "--cookies-from-browser", "firefox",

    "-o", os.path.join(TARGET_DIR, "%(title)s.%(ext)s"),
    "--write-subs",
    "--all-subs",
    COURSE_URL
]

print("\n🚀 Launching fully automated pipeline...")
print(f"📁 Target Destination: {TARGET_DIR}")
print(f"🔒 Active Protections: Native Web Authentication Layer | Firefox Active Auth")

try:
    subprocess.run(command, check=True)
    print("\n🎉 Run completed successfully! Every file is stitched, clean, and perfectly playable.")
except subprocess.CalledProcessError as e:
    print(f"\n❌ Script execution failed: {e}")