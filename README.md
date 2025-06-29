# DigitalDoor Telegram Bot Service

This bot collects questionnaire answers from Telegram users and stores them in Google Sheets. Responses are validated through OpenAI before being accepted.

## Setup
1. Create a `.env` file with the required keys:
   - `TELEGRAM_API_KEY`
   - `OPENAI_KEY`
   - Google service account variables (`GOOGLE_PROJECT_ID`, `GOOGLE_PRIVATE_KEY_ID`, ...)
   - `SHEET_ID` and `SHEET_QUESTIONS`
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the bot:
   ```bash
   python main.py
   ```

## Tests
Run `pytest` to execute the unit tests.
