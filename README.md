
# YouTube Video & Playlist Downloader

## Overview
This project leverages the [pytube](https://pytube.io/en/latest/) library to create a Python-based YouTube video and playlist downloader. Whether you're looking to download a single video or an entire playlist, this script has got you covered!

## Features
- **Single Video Download**: Download any YouTube video by simply providing its URL.
- **Playlist Download**: Download all videos from a YouTube playlist.
- **Progress Bar**: Real-time download progress tracking thanks to the `tqdm` library.
- **Error Handling**: Robust error handling for network issues and video availability.
- **Retry Mechanism**: Auto-retry on network errors.
- **Custom Output Path**: Choose where you want to save your downloaded videos.
- **Logging**: Detailed logs for debugging and auditing.

## Getting Started

### Prerequisites
- Python 3.x
- pip or pip3

### Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/your_username/your_project_name.git
    ```
2. Navigate to the project directory:
    ```bash
    cd your_project_name
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
    or
    ```bash
    pip3 install -r requirements.txt
    ```

### Usage
1. Run the script:
    ```bash
    python main.py
    ```
2. Follow the on-screen prompts to download your video or playlist.

## Configuration
You can set a default download location by editing the `config.ini` file.

## Credits
- Inspired by an article from [Siddharth Chandra](https://blog.codekaro.info/download-youtube-videos-using-python-your-own-youtube-downloader).

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---
