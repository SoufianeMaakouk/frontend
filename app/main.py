# app/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ✅ Allow all origins for now (replace "*" with your frontend URL in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# POST endpoint (button click)
# ------------------------------
class TextInput(BaseModel):
    text: str

SIGN_LANGUAGE_DICT = {
    "hello": "👋 (HELLO sign)",
    "how are you": "🙏 (HOW ARE YOU sign)",
    "thank you": "🤟 (THANK YOU sign)",
    "yes": "👍 (YES sign)",
    "no": "👎 (NO sign)"
}

@app.post("/translate")
async def translate(input: TextInput):
    text = input.text.lower().strip()
    sign = SIGN_LANGUAGE_DICT.get(text, f"❓ (No sign found for '{text}')")
    return {"original": input.text, "sign": sign}

# ------------------------------
# WebSocket endpoint (live translation)
# ------------------------------
@app.websocket("/live-translate")
async def live_translate(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            # Receive live text (or speech-to-text) from frontend
            data = await ws.receive_text()
            text = data.lower().strip()

            # Translate to sign
            sign = SIGN_LANGUAGE_DICT.get(text, f"❓ (No sign found for '{text}')")

            # Send back translation
            await ws.send_json({"original": text, "sign": sign})
    except WebSocketDisconnect:
        print("Client disconnected")
