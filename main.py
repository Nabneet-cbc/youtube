from fastapi import FastAPI
from pytube import YouTube
from fastapi.responses import FileResponse
import os

app = FastAPI()

@app.get("/download")
def download_video():
# Static YouTube URL
    url = "https://www.youtube.com/watch?v=kv7cdS0cEjQ"


    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()

        output_path = "downloads"
        os.makedirs(output_path, exist_ok=True)

        # Download the video
        filepath = stream.download(output_path=output_path)
        filename = os.path.basename(filepath)

        # Return download link or serve the file directly
        return {"download_url": f"/video/{filename}"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/video/{filename}")
def serve_video(filename: str):
    file_path = os.path.join("downloads", filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, media_type='video/mp4', filename=filename)
    return {"error": "File not found"}