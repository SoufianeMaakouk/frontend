# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ✅ Allow all origins for now (you can restrict to your frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class TextInput(BaseModel):
    text: str

# Dummy dictionary for translation
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
