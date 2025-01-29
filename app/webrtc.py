from fastapi import APIRouter, WebSocket
from aiortc import RTCPeerConnection, MediaStreamTrack
import numpy as np
import sounddevice as sd
import asyncio

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

        # Создание RTCPeerConnection для WebRTC
        pc = RTCPeerConnection()
        pc.addTrack(MicrophoneTrack())  # Добавляем поток с микрофона

        @pc.on("iceconnectionstatechange")
        def on_ice_connection_state_change():
            print("ICE connection state:", pc.iceConnectionState)

        @pc.on("icecandidate")
        def on_ice_candidate(candidate):
            if candidate:
                # Отправляем ICE кандидаты клиенту
                asyncio.create_task(websocket.send_text(candidate.sdp))

        # Ожидаем, пока клиент не отправит его SDP-предложение
        offer = await websocket.receive_text()

        # Создаем описание сессии для клиента
        offer = RTCSessionDescription(sdp=offer, type="offer")
        await pc.setRemoteDescription(offer)

        # Генерируем SDP-ответ и отправляем его клиенту
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        await websocket.send_text(answer.sdp)  # Отправка SDP-ответа

        while True:
            await websocket.receive_text()  # Ожидаем другие сообщения от клиента
