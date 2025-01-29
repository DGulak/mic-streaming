from fastapi import APIRouter, WebSocket
from aiortc import RTCPeerConnection, MediaStreamTrack
import numpy as np
import sounddevice as sd

router = APIRouter()

class MicrophoneTrack(MediaStreamTrack):
    kind = "audio"

    def __init__(self):
        super().__init__()
        self.stream = sd.InputStream(channels=1, samplerate=44100)
        self.stream.start()

    async def recv(self):
        frames, _ = self.stream.read(1024)
        return np.frombuffer(frames, dtype=np.int16).tobytes()

class WebRTCConnection:
    def __init__(self):
        self.router = APIRouter()
        self.router.websocket("/ws")(self.websocket_endpoint)

    async def websocket_endpoint(self, websocket: WebSocket):
        await websocket.accept()
        pc = RTCPeerConnection()
        pc.addTrack(MicrophoneTrack())

        while True:
            await websocket.receive_text()