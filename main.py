from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# 🔐 HuggingFace API
HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/facebook/nllb-200-distilled-600M"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# 📦 Request model
class TranslateRequest(BaseModel):
    text: str
    source: str
    target: str

# 🌍 Language code map (IMPORTANT)
lang_map = {
    "en": "eng_Latn",
    "hi": "hin_Deva",
    "bn": "ben_Beng",
    "pa": "pan_Guru",
    "mr": "mar_Deva",
    "ta": "tam_Taml",
    "te": "tel_Telu",
    "gu": "guj_Gujr",
    "kn": "kan_Knda",
    "ml": "mal_Mlym",
    "ur": "urd_Arab",
    "or": "ory_Orya",
    "as": "asm_Beng",
    "ne": "npi_Deva",
    "sa": "san_Deva",
    "sd": "snd_Arab",

    "es": "spa_Latn",
    "fr": "fra_Latn",
    "de": "deu_Latn",
    "zh": "zho_Hans",
    "ja": "jpn_Jpan",
    "ko": "kor_Hang",
    "ar": "arb_Arab",
    "ru": "rus_Cyrl",
    "pt": "por_Latn",
    "it": "ita_Latn",
    "tr": "tur_Latn",
    "nl": "nld_Latn",
    "el": "ell_Grek",
    "th": "tha_Thai",
    "vi": "vie_Latn",
    "id": "ind_Latn",
    "pl": "pol_Latn",
    "sv": "swe_Latn",
    "no": "nob_Latn",
    "fi": "fin_Latn",
    "da": "dan_Latn",
    "he": "heb_Hebr",
    "fa": "pes_Arab",
    "uk": "ukr_Cyrl",
    "ro": "ron_Latn",
    "hu": "hun_Latn",
    "cs": "ces_Latn",
    "sk": "slk_Latn",
    "bg": "bul_Cyrl",
    "sr": "srp_Cyrl",
    "hr": "hrv_Latn",
    "ms": "zsm_Latn",
    "tl": "tgl_Latn",
    "sw": "swh_Latn",
    "af": "afr_Latn"
}

# 🧠 Translation function
def translate_text(text, source, target):
    try:
        src = lang_map.get(source)
        tgt = lang_map.get(target)

        if not src or not tgt:
            return "Language not supported"

        payload = {
            "inputs": text,
            "parameters": {
                "src_lang": src,
                "tgt_lang": tgt
            }
        }

        response = requests.post(API_URL, headers=headers, json=payload, timeout=20)

        result = response.json()

        if isinstance(result, list):
            return result[0]["translation_text"]

        return "Translation error"

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
import os
port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port)