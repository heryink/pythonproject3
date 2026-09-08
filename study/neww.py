import os
import sys
import subprocess
from imageio_ffmpeg import get_ffmpeg_exe

# 1. Directory and Path Pipeline Setup
SKILLJAR_DIR = r"C:\Users\USER\Videos\AI_CORE\Skilljar_Claude_Course"
os.makedirs(SKILLJAR_DIR, exist_ok=True)

COOKIE_FILE = r"C:\Users\USER\Videos\AI_CORE\deep_learning-MIT\cookies.txt"
archive_file = os.path.join(SKILLJAR_DIR, "skilljar_download_history.txt")

# Standard course playlist URL root
COURSE_URL = "https://anthropic.skilljar.com/claude-with-the-anthropic-api"

# 🛠️ CHOOSE WHERE TO START
# Change this number to match the lesson's actual position in the class list
START_INDEX = "15"

venv_dir = os.path.dirname(sys.executable)
yt_dlp_executable = os.path.join(venv_dir, "yt-dlp.exe")
ffmpeg_path = get_ffmpeg_exe()

RESOLUTION_SETTING = "bestvideo[height<=1080]+bestaudio/best"

# 2. Automated Active Cache Cleanup
print("🧼 Automatically clearing temporary download fragments...")
if os.path.exists(SKILLJAR_DIR):
    for item in os.listdir(SKILLJAR_DIR):
        item_path = os.path.join(SKILLJAR_DIR, item)
        if os.path.isfile(item_path) and (item.endswith(".part") or item.endswith(".ytdl")):
            os.remove(item_path)

# 3. Execution Pipeline Payload
command = [
    yt_dlp_executable,
    "-f", RESOLUTION_SETTING,
    "--download-archive", archive_file,
    "--ffmpeg-location", ffmpeg_path,
    "--merge-output-format", "mp4",
    "--concurrent-fragments", "4",
    "--cookies", COOKIE_FILE,
    "--extractor-retries", "3",
    "--fragment-retries", "5",

    # 👇 THE INDEX POINTER: Tells yt-dlp to skip everything before this item number
    "--playlist-start", START_INDEX,

    "-o", os.path.join(SKILLJAR_DIR, "%(chapter_number)s-%(chapter)s_%(title)s.%(ext)s"),
    COURSE_URL
]

print("\n🚀 Launching Target Multi-Threaded Skilljar Downloader Pipeline...")
print(f"📁 Saving to: {SKILLJAR_DIR}")
print(f"🎯 Starting Download From Playlist Item Position: #{START_INDEX}")

try:
    subprocess.run(command, check=True)
    print("\n🎉 Targeted run complete! All subsequent modules saved successfully.")
except subprocess.CalledProcessError as e:
    print(f"\n❌ Pipeline halted: {e}")