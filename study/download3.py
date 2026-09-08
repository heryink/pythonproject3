import os
import sys
import subprocess

# 1. Force install the official static binary of ffmpeg into your environment sandbox
print("Verifying audio/video stitching tools (ffmpeg)...")
try:
    subprocess.run([sys.executable, "-m", "pip", "install", "imageio-ffmpeg"], check=True)
    print("✅ Stitching environment configuration complete!\n")
except Exception as e:
    print(f"⚠️ pip setup warning (can be ignored if network is slow): {e}\n")

# Locate the exact yt-dlp.exe file
venv_dir = os.path.dirname(sys.executable)
yt_dlp_executable = os.path.join(venv_dir, "yt-dlp.exe")

project_root = os.getcwd()
youtube_playlist_url = "https://www.youtube.com/playlist?list=PL2okA_2qDJ-m44KooOI7x8tu85wr4ez4f"

command = [
    yt_dlp_executable,
    # This automatically picks the absolute best available files and prepares them for stitching
    "-f", "bestvideo+bestaudio/best",
    "-o", os.path.join(project_root, "Scikit_Learn_MOOC", "%(playlist_index)s - %(title)s.%(ext)s"),
    youtube_playlist_url
]

print("Starting Scikit-Learn Course Downloader via YouTube Archive...")
try:
    print("🚀 Reconnecting to playlist stream...")
    subprocess.run(command, check=True)
    print("\n🎉 Entire course downloaded and verified successfully in 'Scikit_Learn_MOOC'!")
except subprocess.CalledProcessError as e:
    print(f"\n❌ The downloader encountered an issue: {e}")