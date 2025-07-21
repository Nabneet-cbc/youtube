import os
import uuid
from fastapi import FastAPI
from pytube import YouTube
import whisper

# ✅ FFmpeg setup for Render
os.environ["PATH"] += os.pathsep + os.path.join(os.path.expanduser("~"), ".local", "bin")
from ffmpeg_downloader import download_ffmpeg
download_ffmpeg()

app = FastAPI()

# ✅ Static YouTube URL (replace this with your own)
STATIC_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

@app.get("/")
def home():
    return {"message": "YouTube Audio Transcription API"}

@app.get("/transcribe")
def transcribe_youtube():
    # ✅ Step 1: Download audio
    yt = YouTube(STATIC_URL)
    stream = yt.streams.filter(only_audio=True).first()

    filename = f"{uuid.uuid4()}.mp4"
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    stream.download(output_path=output_dir, filename=filename)

    # ✅ Step 2: Transcribe
    model = whisper.load_model("tiny")  # faster, lower RAM
    result = model.transcribe(filepath)

    # ✅ Step 3: Cleanup
    os.remove(filepath)

    return {"transcription": result["text"]}
