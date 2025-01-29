from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse  # Добавить импорт StreamingResponse
import sounddevice as sd
import numpy as np
import io

app = FastAPI()

# Обработчик для корневого маршрута, отдающий HTML-файл
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("static/index.html", "r") as f:  # Убедитесь, что путь правильный
        return HTMLResponse(content=f.read())

def audio_stream():
    while True:
        frames, _ = sd.rec(1024, samplerate=48000, channels=1, dtype='int16', blocking=True)
        wav_buffer = io.BytesIO()
        wav_buffer.write(frames.tobytes())
        wav_buffer.seek(0)
        yield wav_buffer.read()

@app.get("/stream")
def stream_audio():
    return StreamingResponse(audio_stream(), media_type="audio/wav")
