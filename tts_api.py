from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from gtts import gTTS
from io import BytesIO

app = FastAPI(title="gTTS Text-to-Speech API")

@app.get("/speak", response_class=StreamingResponse)
def speak(text: str = Query(..., min_length=1, max_length=500), lang: str = "en"):
    """
    Stream TTS audio for the given text and language.
    Example: /speak?text=Hello+world&lang=en
    """
    tts = gTTS(text=text, lang=lang)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return StreamingResponse(mp3_fp, media_type="audio/mpeg")

@app.get("/health")
def health():
    return {"status": "ok"}
