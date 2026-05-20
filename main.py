from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
import time

app = FastAPI()

# ❌ HuggingFace remove
# HF_TOKEN = os.getenv("HF_TOKEN")

# ✅ LibreTranslate API
API_URL = "https://libretranslate.com/translate"

headers = {
    "Content-Type": "application/json"
}

# 📦 Request model
class TranslateRequest(BaseModel):
    text: str
    source: str
    target: str

# 🌍 Language code map (same rakha hai)
lang_map = {
    "en": "en",
    "hi": "hi",
    "bn": "bn",
    "pa": "pa",
    "mr": "mr",
    "ta": "ta",
    "te": "te",
    "gu": "gu",
    "kn": "kn",
    "ml": "ml",
    "ur": "ur",
    "or": "or",
    "as": "as",
    "ne": "ne",
    "sa": "sa",
    "sd": "sd",

    "es": "es",
    "fr": "fr",
    "de": "de",
    "zh": "zh",
    "ja": "ja",
    "ko": "ko",
    "ar": "ar",
    "ru": "ru",
    "pt": "pt",
    "it": "it",
    "tr": "tr",
    "nl": "nl",
    "el": "el",
    "th": "th",
    "vi": "vi",
    "id": "id",
    "pl": "pl",
    "sv": "sv",
    "no": "no",
    "fi": "fi",
    "da": "da",
    "he": "he",
    "fa": "fa",
    "uk": "uk",
    "ro": "ro",
    "hu": "hu",
    "cs": "cs",
    "sk": "sk",
    "bg": "bg",
    "sr": "sr",
    "hr": "hr",
    "ms": "ms",
    "tl": "tl",
    "sw": "sw",
    "af": "af"
}

# 🔁 Retry API call (same logic)
def call_api(payload):
    for i in range(3):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            return response
        except Exception as e:
            print("Retrying...", e)
            time.sleep(2)
    return None

# 🧠 Translation function
def translate_text(text, source, target):
    try:
        src = lang_map.get(source)
        tgt = lang_map.get(target)

        if not src or not tgt:
            return "Language not supported"

        payload = {
            "q": text,
            "source": src,
            "target": tgt,
            "format": "text"
        }

        response = call_api(payload)

        if response is None:
            return "Server network error"

        result = response.json()

        print("RAW RESPONSE:", result)

        # ✅ Success
        if "translatedText" in result:
            return result["translatedText"]

        # ❌ Error
        if "error" in result:
            return result["error"]

        return "Unknown error"

    except Exception as e:
        return str(e)

# 🚀 API endpoint
@app.post("/translate")
def translate(req: TranslateRequest):
    translated = translate_text(req.text, req.source, req.target)
    return {"translated_text": translated}

# 🩺 Health check
@app.get("/")
def home():
    return {"status": "API is running 🚀"}

# 🔌 Render PORT fix
port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port)