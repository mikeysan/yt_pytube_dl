from pytube import YouTube as yt




def get_stream_from_res(streams, res):
    """
    Filter the video stream based on resolution
    """
    stream = list(filter(lambda x: x.resolution == res, streams))

    return stream if stream else None
    

video_url = input("Enter the video url: ")
youtube_obj = yt(video_url)

video_res = input(f"Enter the video resolution for {youtube_obj.title}: ").strip()



req_stream = get_stream_from_res(youtube_obj.streams, video_res)[0] # pylint: disable=unsubscriptable-object

print()
print(f"\nDownloading {youtube_obj.title} ...")

# req_stream.download("[add full path]")
req_stream.download()
print(f"Youtube video: {youtube_obj.title} and Resolution: {video_res} downloaded successfully")



# Sample link to play with
# https://www.youtube.com/watch?v=q4Xrs4iVA0Q
# https://www.youtube.com/watch?v=YXPyB4XeYLA
