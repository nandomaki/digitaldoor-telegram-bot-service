import os
from dotenv import load_dotenv
import logging

load_dotenv()

# Telegram
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")

# OpenAI
OPENAI_KEY = os.getenv("OPENAI_KEY")

# Google Service Account
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
GOOGLE_PRIVATE_KEY_ID = os.getenv("GOOGLE_PRIVATE_KEY_ID")
GOOGLE_PRIVATE_KEY = os.getenv("GOOGLE_PRIVATE_KEY")
GOOGLE_CLIENT_EMAIL = os.getenv("GOOGLE_CLIENT_EMAIL")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
SHEET_ID = os.getenv("SHEET_ID")
SHEET_QUESTIONS = os.getenv("SHEET_QUESTIONS")

# Basic logging configuration
logging.basicConfig(level=logging.INFO)
