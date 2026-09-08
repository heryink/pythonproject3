import os
import sys
import subprocess

# Locate the exact yt-dlp.exe file
venv_dir = os.path.dirname(sys.executable)
yt_dlp_executable = os.path.join(venv_dir, "yt-dlp.exe")

# This dynamically finds the absolute path to your main PythonProject3 folder
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cookies_file = os.path.join(project_root, "cookies.txt")

command = [
    yt_dlp_executable,
    "--cookies", cookies_file,
    "-f", "bestvideo+bestaudio/best",
    "-o", os.path.join(project_root, "MOOC_Videos", "%(playlist_index)s - %(title)s.%(ext)s"),
    "https://lms.fun-mooc.fr/courses/course-v1:inria+41026+session04/courseware/"
]

print("Starting FUN-MOOC Course Downloader...")
print(f"Searching for file at: {cookies_file}")

if not os.path.exists(cookies_file):
    print(f"❌ Error: Could not find 'cookies.txt' at {cookies_file}")
else:
    try:
        print("✅ Found cookies.txt! Connecting to FUN-MOOC servers...")
        subprocess.run(command, check=True)
        print("\n🎉 All videos downloaded successfully into your 'MOOC_Videos' folder!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ The downloader encountered an issue: {e}")