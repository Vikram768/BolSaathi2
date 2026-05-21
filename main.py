from fastapi import FastAPI
from pydantic import BaseModel
import os
import time

# ✅ NLLB imports
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

app = FastAPI()

# 📦 Request model (same)
class TranslateRequest(BaseModel):
    text: str
    source: str
    target: str

# 🌍 Language code map (same as NLLB version)
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

# 🔥 LOAD MODEL (optimized smaller model)
MODEL_NAME = "facebook/nllb-200-distilled-600M"

print("Loading NLLB model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# ⚡ CPU optimization
torch.set_num_threads(4)

print(f"Model loaded on {device}")

# 🔥 Warm-up (remove first request delay)
print("Warming up model...")
_dummy = tokenizer("Hello", return_tensors="pt").to(device)
with torch.inference_mode():
    model.generate(**_dummy, max_length=20)

# ⚡ Cache for repeated requests
cache = {}

# 🧠 Translation function (optimized)
def translate_text(text, source, target):
    try:
        key = f"{text}_{source}_{target}"

        # ⚡ cache check
        if key in cache:
            return cache[key]

        source_lang = lang_map.get(source)
        target_lang = lang_map.get(target)

        if not source_lang or not target_lang:
            return "Unsupported language"

        tokenizer.src_lang = source_lang

        inputs = tokenizer(text, return_tensors="pt", truncation=True).to(device)

        # ⚡ FAST inference
        with torch.inference_mode():
            translated_tokens = model.generate(
                **inputs,
                forced_bos_token_id=tokenizer.convert_tokens_to_ids(target_lang),
                max_length=256
            )

        output = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)

        result = output[0]

        # ⚡ save to cache
        cache[key] = result

        return result

    except Exception as e:
        return str(e)

# 🚀 API endpoint (same)
@app.post("/translate")
def translate(req: TranslateRequest):
    translated = translate_text(req.text, req.source, req.target)
    return {"translated_text": translated}

# 🩺 Health check (same)
@app.get("/")
def home():
    return {"status": "NLLB API is running 🚀"}

# 🔌 Render PORT fix (same)
port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port)