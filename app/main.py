from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.webrtc import WebRTCConnection

app = FastAPI()

# Подключение статических файлов (HTML)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Инициализация WebRTC
webrtc = WebRTCConnection()
app.include_router(webrtc.router)

@app.get("/")
async def root():
    return {"message": "Microphone Streaming Service is running!"}