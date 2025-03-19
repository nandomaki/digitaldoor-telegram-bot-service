import telebot
import os
from dotenv import load_dotenv

load_dotenv()
CHAVE_API = os.getenv("TELEGRAM_API_KEY")

def bot_teste():
    bot = telebot.TeleBot(CHAVE_API)

    @bot.message_handler(commands=["opcao1"])
    def opcao1(messagem):
        bot.reply_to(messagem, "opcao 1")
        pass

    @bot.message_handler(commands=["opcao2"])
    def opcao2(messagem):
        pass

    @bot.message_handler(commands=["opcao3"])
    def opcao3(messagem):
        pass



    def verificar(mensagem):
        return True

    @bot.message_handler(func=verificar)
    def responder(messagem):

        texto = """Escolha a opção:
        /opcao1: Luiz,
        /opcao2: Fernando,
        /opcao3: Elon,"""

        bot.reply_to(messagem, texto)

    bot.polling()

