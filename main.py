import os
import uuid
from fastapi import FastAPI, Query
from pytube import YouTube

app = FastAPI()

@app.get("/")
def home():
    return {"message": "YouTube Video Downloader API is running."}

@app.get("/download")
def download_youtube_video(url: str = Query(...)):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()

        os.makedirs("downloads", exist_ok=True)
        filename = f"{uuid.uuid4()}.mp4"
        filepath = os.path.join("downloads", filename)

        stream.download(output_path="downloads", filename=filename)

        return {
            "message": "Video downloaded successfully",
            "video_title": yt.title,
            "filename": filename,
            "filepath": filepath
        }

    except Exception as e:
        return {"error": str(e)}
