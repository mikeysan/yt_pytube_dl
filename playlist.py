from pytube import Playlist, YouTube
from tqdm import tqdm


def download_video(video_obj, output_path):
    """
    Download a single video
    """
    print(f"\nDownloading {video_obj.title} ...")
    video_obj.streams.get_highest_resolution().download(output_path)
    print(f"Video: {video_obj.title} downloaded successfully")


def download_playlist(playlist_url, output_path):
    """
    Download an entire playlist
    """
    playlist = Playlist(playlist_url)
    playlist.populate_video_urls()

    print(f"\nDownloading playlist: {playlist.title} ...")

    for video_url in tqdm(playlist.video_urls, unit="video"):
        try:
            video = YouTube(video_url)
            download_video(video, output_path)
        except Exception as e:
            print(f"Error downloading {video_url}: {str(e)}")

    print(f"\nPlaylist: {playlist.title} downloaded successfully")


# Prompt the user for inputs
is_playlist = input("Is it a playlist? (Y/N): ").strip().lower() == "y"
url = input("Enter the URL: ").strip()
output_path = input("Enter the output path: ").strip()

# Download video or playlist based on user input
if is_playlist:
    download_playlist(url, output_path)
else:
    video = YouTube(url)
    download_video(video, output_path)
