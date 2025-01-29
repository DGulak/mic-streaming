import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
# Храним активный поток аудио (по сути - очередь)
audio_stream = asyncio.Queue()

# Эндпоинт для передачи HTML страницы
@app.get("/")
async def get_index():
    return HTMLResponse(content=open("static/index.html").read(), status_code=200)

# WebSocket для принятия аудио потока от клиента
@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Получаем аудио данные от клиента
            audio_data = await websocket.receive_bytes()
            # Добавляем данные в очередь (по сути, это и есть поток)
            await audio_stream.put(audio_data)
    except WebSocketDisconnect:
        print("Client disconnected")
        await websocket.close()

# Эндпоинт для получения текущего аудио потока
@app.get("/stream")
async def get_audio_stream():
    if not audio_stream.empty():
        # Получаем аудио данные из очереди
        audio_data = await audio_stream.get()
        return StreamingResponse(iter([audio_data]), media_type="audio/wav")
    else:
        # Возвращаем пустой поток, если нет данных
        return StreamingResponse(iter([]), media_type="audio/wav")
