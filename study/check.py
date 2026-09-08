import os

# Define the target paths used by your downloader setup
TARGET_DIR = r"C:\Users\USER\Videos\AI_CORE\deep_learning-MIT"
ARCHIVE_FILE = os.path.join(TARGET_DIR, "downloaded_history.txt")

print("🔍 Analyzing local download directory setup...")

# 1. Count physical .mp4 video files sitting on your drive
mp4_files = []
if os.path.exists(TARGET_DIR):
    mp4_files = [f for f in os.listdir(TARGET_DIR) if f.endswith('.mp4')]
    print(f"📁 Video Files (.mp4) Found on Disk: {len(mp4_files)}")
else:
    print(f"❌ Error: The directory '{TARGET_DIR}' does not exist.")

# 2. Count recorded successful downloads inside the history tracking archive
archive_count = 0
if os.path.exists(ARCHIVE_FILE):
    with open(ARCHIVE_FILE, 'r', encoding='utf-8') as f:
        # Each line represents a successfully completed and stitched video ID
        archive_count = len([line for line in f if line.strip()])
    print(f"📝 Completed Video IDs in History Log: {archive_count}")
else:
    print("📝 History Log Status: No tracking archive file created yet.")

# 3. Final Reconciliation Output
print("\n--- Summary Results ---")
if len(mp4_files) == 90 and archive_count == 90:
    print("🎉 Success! Every single one of the 90 videos is 100% downloaded and ready.")
else:
    print(f"⚠️ Your course is incomplete. You currently have {len(mp4_files)} of 90 items.")
    print("💡 Fix: Make sure your internet is stable and run your main download script again.")