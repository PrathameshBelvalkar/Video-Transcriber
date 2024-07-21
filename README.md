# Video Transcriber

## Overview

The Video Transcriber is a Python application that transcribes audio from video files into subtitles. It uses the Whisper model from OpenAI for transcription and generates an SRT file with subtitles. The application provides a graphical user interface using `tkinter`.

## Features

- Extracts audio from video files.
- Transcribes audio to text using Whisper.
- Generates SRT subtitles file.

## Requirements

Ensure you have Python installed. The following Python libraries are required:

- `moviepy` for audio extraction.
- `torch` for machine learning operations.
- `whisper` for transcription.

You can install the required libraries using the provided `requirements.txt` file.

## Installation

1. Clone the repository or download the source code.

2. Navigate to the project directory.

3. Install the required libraries:
```bash
pip install -r requirements.txt
```

## Usage
1. Run the application:
``` bash
python GUI.py
```
2. In the application:
- Click the "Browse" button to select a video file.
- Click the "Process" button to start transcription.

3. The text area will display a message indicating that subtitles are being processed and will update once the processing is complete. The SRT file will be named as the video file name with an .srt extension and saved in the same directory as the video file.

## File Naming Convention
The generated subtitles file will be named according to the video file name with the .srt extension. For example, if the video file is named `example.mp4`, the subtitle file will be `example.srt`.


