from fastapi import FastAPI
from pydantic import BaseModel
import os
import time
import requests   # (kept same as you had)

app = FastAPI()

# 📦 Request model (same)
class TranslateRequest(BaseModel):
    text: str
    source: str
    target: str

# 🌍 Language code map (kept SAME as your version)
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

# ⚡ Cache (same)
cache = {}

# ============================
# 🔥 ARGOS TRANSLATE ADDED
# ============================
import argostranslate.package
import argostranslate.translate

def install_argos_models():
    try:
        installed = argostranslate.translate.get_installed_languages()

        # install only once
        if len(installed) == 0:
            print("Installing Argos models...")

            packages = argostranslate.package.get_available_packages()

            for pkg in packages:
                # install common pairs (expand later if needed)
                if (pkg.from_code == "en" and pkg.to_code == "hi") or \
                   (pkg.from_code == "hi" and pkg.to_code == "en"):

                    download_path = pkg.download()
                    argostranslate.package.install_from_path(download_path)

            print("Argos installed ✅")

    except Exception as e:
        print("Argos install error:", e)

# 🧠 Translation function (UPDATED → Argos first, HF fallback removed)
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

        # ============================
        # 🔥 ARGOS TRANSLATION ENGINE
        # ============================
        translated = argostranslate.translate.translate(
            text,
            source_lang,
            target_lang
        )

        cache[key] = translated
        return translated

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
    return {"status": "Argos API running 🚀"}

# 🔌 Render PORT fix (same)
port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    import uvicorn
    install_argos_models()   # 🔥 ensure models before start
    uvicorn.run("main:app", host="0.0.0.0", port=port)