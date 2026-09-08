import subprocess
import sys


def download_mit_linear_algebra(output_dir="MIT_18.06_Linear_Algebra"):
    """
    Download all video lectures of MIT 18.06 Linear Algebra from YouTube.
    Uses the official MIT OpenCourseWare playlist.
    """
    playlist_url = "https://www.youtube.com/playlist?list=PL49CF3715CB9EF31D"

    # Create output directory
    import os
    os.makedirs(output_dir, exist_ok=True)

    # yt-dlp command
    cmd = [
        "yt-dlp",
        "--ignore-errors",
        "--format", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--output", f"{output_dir}/%(playlist_index)02d - %(title)s.%(ext)s",
        "--write-auto-sub",  # Download subtitles if available
        "--sub-lang", "en",
        "--embed-subs",  # Embed subtitles into video (optional)
        "--merge-output-format", "mp4",
        playlist_url
    ]

    print(f"Downloading playlist from: {playlist_url}")
    print(f"Saving to: {output_dir}/")
    print("Press Ctrl+C to stop at any time.\n")

    try:
        subprocess.run(cmd, check=True)
        print("\nDownload completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nDownload interrupted by user.")
        sys.exit(0)


if __name__ == "__main__":
    # You can change the output directory by passing an argument
    output = "MIT_18.06_Linear_Algebra"
    if len(sys.argv) > 1:
        output = sys.argv[1]
    download_mit_linear_algebra(output)