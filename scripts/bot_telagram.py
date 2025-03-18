import telebot
import os
from dotenv import load_dotenv

load_dotenv()
CHAVE_API = os.getenv("TELEGRAM_API_KEY")

def bot_teste():
    bot = telebot.TeleBot(CHAVE_API)

    @bot.message_handler(commands=['ola'])
    def responder(messagem):
        bot.reply_to(messagem, 'Hello world')

    bot.polling()

