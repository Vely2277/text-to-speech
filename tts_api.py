from fastapi import FastAPI, Form, BackgroundTasks
from kitten_tts import TTS
from fastapi.responses import FileResponse
import io
import tempfile
import os

app = FastAPI()
tts = TTS()

@app.post("/speak")
async def speak(text: str = Form(...), background_tasks: BackgroundTasks):
    from asyncio import to_thread
    audio_bytes = await to_thread(tts.speak, text)

    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    # Schedule file deletion after response
    background_tasks.add_task(os.remove, tmp_path)

    return FileResponse(
        path=tmp_path,
        media_type="audio/mpeg",
        filename="speech.mp3"
    )