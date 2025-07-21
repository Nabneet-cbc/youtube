import os
import uuid
from fastapi import FastAPI
from pytube import YouTube
import whisper

app = FastAPI()

STATIC_URL = "https://www.youtube.com/watch?v=ScKCy2udln8"

@app.get("/")
def home():
    return {"message": "YouTube Audio Transcription API"}

@app.get("/transcribe")
def transcribe_youtube():
    yt = YouTube(STATIC_URL)
    stream = yt.streams.filter(only_audio=True).first()

    filename = f"{uuid.uuid4()}.mp4"
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    stream.download(output_path=output_dir, filename=filename)

    model = whisper.load_model("tiny")
    result = model.transcribe(filepath)

    os.remove(filepath)
    return {"transcription": result["text"]}
