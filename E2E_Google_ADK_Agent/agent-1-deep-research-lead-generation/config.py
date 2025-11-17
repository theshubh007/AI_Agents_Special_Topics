import os
from dotenv import load_dotenv

load_dotenv()

GEN_ADVANCED_MODEL = os.getenv("GEN_ADVANCED_MODEL", "gemini-2.5-flash")
GEN_FAST_MODEL = os.getenv("GEN_FAST_MODEL", "gemini-2.5-flash")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is required")
