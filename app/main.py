from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
import sounddevice as sd
import numpy as np
import io

app = FastAPI()

# Обработчик для корневого маршрута, отдающий HTML-файл
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("index.html", "r") as f:  # Предполагается, что файл находится в корне проекта
        return HTMLResponse(content=f.read())

def audio_stream():
    while True:
        frames = sd.rec(1024, samplerate=48000, channels=1, dtype='int16', blocking=True)
        wav_buffer = io.BytesIO()
        wav_buffer.write(frames.tobytes())
        wav_buffer.seek(0)
        yield wav_buffer.read()

@app.get("/stream")
def stream_audio():
    return StreamingResponse(audio_stream(), media_type="audio/wav")
