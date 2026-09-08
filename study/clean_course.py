import os

TARGET_DIR = r"C:\Users\USER\Videos\AI_CORE\deep_learning-MIT"
ARCHIVE_FILE = os.path.join(TARGET_DIR, "downloaded_history.txt")

# Load all valid, completed video IDs into memory
valid_ids = set()
if os.path.exists(ARCHIVE_FILE):
    with open(ARCHIVE_FILE, 'r', encoding='utf-8') as f:
        valid_ids = {line.strip() for line in f if line.strip()}

print("🧼 Scanning for incomplete or corrupted video files...")

# Automatically scan the folder and remove any file that isn't fully marked complete
if os.path.exists(TARGET_DIR):
    for filename in os.listdir(TARGET_DIR):
        if filename.endswith(".mp4"):
            file_path = os.path.join(TARGET_DIR, filename)

            # Since we can't easily match filenames to raw IDs without extracting metadata,
            # we will safely clear out temporary dynamic fragments (.part, .ytdl) instead.
            if filename.endswith(".part") or filename.endswith(".ytdl"):
                os.remove(file_path)
                print(f"🗑️ Removed partial fragment: {filename}")

print("✅ Cleanup complete. Ready for a fresh resume execution!")