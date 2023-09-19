from pytube import Playlist, YouTube
from tqdm import tqdm
import logging
import time
from retrying import retry
import configparser
import os
import validators
from requests.exceptions import ConnectionError
from pytube.exceptions import VideoUnavailable



config = configparser.ConfigParser()
config.read('config.ini')

default = config.get('DEFAULT', 'download_location')

logging.basicConfig(filename='yt_downloader.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')


def validate_url(url):
    """
    Validate a URL
    """
    if not validators.url(url):
        raise ValueError(f"Invalid URL: {url}")


def validate_output_path(output_path):
    """
    Validate an output path
    """
    if not os.path.isdir(output_path):
        raise ValueError(f"Invalid output path: {output_path}")
    if not os.access(output_path, os.W_OK):
        raise ValueError(f"Output path is not writable: {output_path}")


def progress_callback(stream, chunk, bytes_remaining):
    global progress_bar
    current_progress = progress_bar.total - bytes_remaining
    progress_bar.update(current_progress - progress_bar.n)  # update progress


@retry(stop_max_attempt_number=3, wait_fixed=2000, retry_on_exception=lambda e: isinstance(e, ConnectionError))
def download_video(video_obj, output_path):
    """
    Download a single video
    """
    try:
        print(f"\nDownloading {video_obj.title} ...")
    
        # Create a tqdm progress bar
        global progress_bar
        progress_bar = tqdm(total=video_obj.streams.get_highest_resolution().filesize, unit='B', unit_scale=True)
    
        # Register the progress callback
        video_obj.register_on_progress_callback(progress_callback)
    
        video_obj.streams.get_highest_resolution().download(output_path)
        print(f"Video: {video_obj.title} downloaded successfully")
    
        # Close the progress bar
        progress_bar.close()
    except VideoUnavailable as e:
        logging.error(f"Video {video_obj.title} is unavailable: {str(e)}")
    except ConnectionError as e:
        logging.error(f"Network error when downloading video {video_obj.title}: {str(e)}")
        raise  # re-raise the exception to trigger retry
    except Exception as e:
        logging.error(f"Unexpected error when downloading video {video_obj.title}: {str(e)}")


def get_playlist(playlist_url):
    """
    Get a playlist from a URL
    """
    playlist = Playlist(playlist_url)
    return playlist


def iterate_videos(playlist, output_path):
    """
    Iterate over videos in a playlist and download each one
    """
    print(f"\nDownloading playlist: {playlist.title} ...")

    for video_url in tqdm(playlist.video_urls, unit="video"):
        try:
            video = YouTube(video_url)
            download_video(video, output_path)
        except Exception as e:
            logging.error(f"Error downloading {video_url}: {str(e)}")

    print(f"\nPlaylist: {playlist.title} downloaded successfully")


def download_playlist(playlist_url, output_path):
    """
    Download an entire playlist
    """
    playlist = get_playlist(playlist_url)
    iterate_videos(playlist, output_path)


def get_user_inputs():
    """
    Prompt the user for inputs and return them
    """
    is_playlist = input("Is it a playlist? (Y/N): ").strip().lower() == "y"
    url = input("Enter the URL: ").strip()
    output_path = input("Use the default location or Enter the output path: ").strip()

    # If no output path, use the default
    if output_path == "":
        output_path = default

    # Validate the inputs
    validate_url(url)
    validate_output_path(output_path)

    return is_playlist, url, output_path



def main():
    # Get user inputs
    is_playlist, url, output_path = get_user_inputs()


    # Download video or playlist based on user input
    if is_playlist:
        download_playlist(url, output_path)
    else:
        video = YouTube(url)
        download_video(video, output_path)


if __name__ == "__main__":
    main()
