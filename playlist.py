from pytubefix import Playlist, YouTube
from tqdm import tqdm
import logging
import time
from retrying import retry
import configparser
import os
import subprocess
import tempfile
import validators
from urllib.error import URLError
from pytubefix.exceptions import VideoUnavailable, MaxRetriesExceeded
from pytubefix.helpers import safe_filename



config = configparser.ConfigParser()
config.read('config.ini')

default = config.get('DEFAULT', 'download_location')

# MWEB serves the highest resolution streams as direct downloads (others use SABR or get 403s mid-file)
CLIENT = 'MWEB'

# pytubefix uses urllib, so these (not requests' ConnectionError) are what a network failure raises
NETWORK_ERRORS = (URLError, MaxRetriesExceeded, ConnectionError, TimeoutError)

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
    progress_bar.update(len(chunk))  # update progress


@retry(stop_max_attempt_number=3, wait_fixed=2000, retry_on_exception=lambda e: isinstance(e, NETWORK_ERRORS))
def download_video(video_obj, output_path):
    """
    Download the highest resolution video and best audio, then merge them with ffmpeg
    """
    try:
        output_file = os.path.join(output_path, f"{safe_filename(video_obj.title)}.mp4")
        if os.path.exists(output_file):
            print(f"\nVideo: {video_obj.title} already exists, skipping")
            return

        print(f"\nDownloading {video_obj.title} ...")

        video_stream = video_obj.streams.get_highest_resolution(progressive=False)
        audio_stream = video_obj.streams.get_audio_only()

        # Create a tqdm progress bar covering both the video and audio downloads
        global progress_bar
        progress_bar = tqdm(total=video_stream.filesize + audio_stream.filesize, unit='B', unit_scale=True)

        # Register the progress callback
        video_obj.register_on_progress_callback(progress_callback)

        with tempfile.TemporaryDirectory() as temp_dir:
            video_file = video_stream.download(temp_dir, filename_prefix='video_')
            audio_file = audio_stream.download(temp_dir, filename_prefix='audio_')

            # Close the progress bar
            progress_bar.close()

            # Merge the separate video and audio streams without re-encoding
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video_file, '-i', audio_file,
                            '-c', 'copy', output_file], check=True)

        print(f"Video: {video_obj.title} downloaded successfully")
    except VideoUnavailable as e:
        logging.error(f"Video {video_obj.title} is unavailable: {str(e)}")
    except NETWORK_ERRORS as e:
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
            video = YouTube(video_url, client=CLIENT)
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
        video = YouTube(url, client=CLIENT)
        download_video(video, output_path)


if __name__ == "__main__":
    main()
