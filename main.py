from pytube import YouTube as yt



def get_video_from_res(streams, res):
    """
    Filter resulting video stream based on resolution
    """
    stream = list(filter(lambda x: x.resolution == res, streams))

    return stream if stream else None
    

video_url = input("Enter the video url: ")
youtube_obj = yt(video_url)

# Ask user for resolution to search. E.g. 720p, 1080p
video_res = input(f"Enter the video resolution for {youtube_obj.title}: ").strip()


# Call get_video_from_res function
req_stream = get_video_from_res(youtube_obj.streams, video_res)[0] # pylint: disable=unsubscriptable-object

# Print a blank line followed by another line telling the user download has started
print("\n")
print(f"\nDownloading {youtube_obj.title} ...")

# Call the download function without specifying a path
# No path specified means downloaded file(s) will be saved to current directory or script
# Alternatively you can specify a path using the example shown below
# req_stream.download("[add full path]")
req_stream.download()

# Print a final message to let the user know download is complete
print(f"Youtube video: {youtube_obj.title} and Resolution: {video_res} downloaded successfully")



# Sample links to play with
# https://www.youtube.com/watch?v=q4Xrs4iVA0Q
# https://www.youtube.com/watch?v=YXPyB4XeYLA
