import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
NUMBER_OF_INTERVIEW_QUESTIONS = int(os.getenv("NUMBER_OF_INTERVIEW_QUESTIONS", "10"))
LLM_MODEL = "google/gemini-2.5-flash"
#LLM_MODEL = "x-ai/grok-3-beta"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN manquant dans .env")
if not OPENROUTER_KEY:
    raise RuntimeError("OPENROUTER_KEY manquant dans .env")
