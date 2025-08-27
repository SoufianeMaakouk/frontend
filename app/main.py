# app/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SIGN_LANGUAGE_DICT = {
    "hello": "👋 (HELLO sign)",
    "yes": "👍 (YES sign)",
    "no": "👎 (NO sign)"
}

class TextInput(BaseModel):
    text: str

@app.post("/translate")
async def translate(input: TextInput):
    text = input.text.lower().strip()
    sign = SIGN_LANGUAGE_DICT.get(text, f"❓ (No sign found for '{text}')")
    return {"original": input.text, "sign": sign}

# --- New route for audio ---
@app.post("/audio_translate")
async def audio_translate(audio: UploadFile = File(...)):
    # Here you would process audio with a speech-to-text AI model
    # For now, let's assume it always says "hello"
    recognized_text = "hello"
    sign = SIGN_LANGUAGE_DICT.get(recognized_text, f"❓ (No sign found)")
    return {"original": recognized_text, "sign": sign}
