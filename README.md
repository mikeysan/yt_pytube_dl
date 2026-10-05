
# YouTube Video & Playlist Downloader

## Overview
This project leverages the [pytubefix](https://pytubefix.readthedocs.io/) library to create a Python-based YouTube video and playlist downloader. Whether you're looking to download a single video or an entire playlist, this script has got you covered!

## Features
- **Single Video Download**: Download any YouTube video by simply providing its URL.
- **Playlist Download**: Download all videos from a YouTube playlist.
- **Highest Quality**: Downloads the highest resolution video available (up to 4K) and the best audio, then merges them into a single `.mp4` with `ffmpeg` (no re-encoding).
- **Skips Existing Videos**: Videos already in the output folder are skipped, so an interrupted playlist picks up where it left off.
- **Progress Bar**: Real-time download progress tracking thanks to the `tqdm` library.
- **Error Handling**: Robust error handling for network issues and video availability.
- **Retry Mechanism**: Auto-retry on network errors (up to 3 attempts per video).
- **Custom Output Path**: Choose where you want to save your downloaded videos.
- **Logging**: Detailed logs for debugging and auditing, written to `yt_downloader.log`.

## Getting Started

### Prerequisites
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (it will install Python 3.10+ for you if needed)
- [ffmpeg](https://ffmpeg.org/download.html) on your `PATH` (used to merge the separate video and audio streams)

### Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/mikeysan/yt_pytube_dl.git
    ```
2. Navigate to the project directory:
    ```bash
    cd yt_pytube_dl
    ```
3. Install the required packages:
    ```bash
    uv sync
    ```

### Usage
1. Run the script:
    ```bash
    uv run playlist.py
    ```
2. Follow the on-screen prompts to download your video or playlist.

## Configuration
You can set a default download location by editing the `config.ini` file. It is used when you leave the output path blank at the prompt:
```ini
[DEFAULT]
download_location = /path/to/your/downloads
```

## Troubleshooting
YouTube regularly changes how it serves video to different clients. If downloads start failing with `HTTP Error 403: Forbidden`, try changing `CLIENT` near the top of `playlist.py` (for example, to `VISION_OS`) and update pytubefix with `uv lock --upgrade-package pytubefix && uv sync`.

## Credits
- Inspired by an article from [Siddharth Chandra](https://blog.codekaro.info/download-youtube-videos-using-python-your-own-youtube-downloader).

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---
