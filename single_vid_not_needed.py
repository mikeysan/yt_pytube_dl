# This code is NOT needed, but I haven't had time to go through it since moving everything to the playlist version.

from pytube import YouTube as yt
from tqdm import tqdm


def get_stream_from_res(streams, res):
    """
    Filter the video stream based on resolution
    """
    stream = list(filter(lambda x: x.resolution == res, streams))

    return stream if stream else None
    

video_url = input("Enter the video url: ")
youtube_obj = yt(video_url)

video_res = input(f"Enter the video resolution for {youtube_obj.title}: ").strip()

# Get the stream
stream = get_stream_from_res(youtube_obj.streams, video_res)

# Check if a stream was found
if stream is not None:
    req_stream = stream[0]
    print()
    print(f"\nDownloading {youtube_obj.title} ...")

    # Create a progress bar
    progress_bar = tqdm(total=req_stream.filesize, unit='bytes', unit_scale=True)

    def progress_callback(stream, chunk, bytes_remaining):
        # Calculate the length of the chunk indirectly
        length = req_stream.filesize - bytes_remaining

        # Update the progress bar
        progress_bar.update(length - progress_bar.n)

    # Set the progress callback function
    req_stream.on_progress = progress_callback

    # Start the download
    req_stream.download("/home/sspade/Downloads/yt")

    # Close the progress bar
    progress_bar.close()

    print(f"Youtube video: {youtube_obj.title} and Resolution: {video_res} downloaded successfully")
else:
    print(f"No stream found for {youtube_obj.title} at resolution {video_res}")


