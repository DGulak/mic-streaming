from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import sounddevice as sd
import numpy as np
import io

app = FastAPI()

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