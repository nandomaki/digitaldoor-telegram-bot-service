import telebot
import os
from dotenv import load_dotenv
from scripts.datasheet_services import DataSheetServices
from constants.questions import QUESTIONS, NUMERO_MAXIMO_QUESTOES

load_dotenv()
CHAVE_API = os.getenv("TELEGRAM_API_KEY")
bot = telebot.TeleBot(CHAVE_API)

datasheet = DataSheetServices()

@bot.message_handler(commands=['options'])
def options(message):
    text = """Escolha as opções que deseja fazer:

    1 - /addNewUser para adicionar um novo usuário
    2- /deleteUser para deletar um usuário
        
    Clique na opção desejada....
    """
    bot.reply_to(message, text)

@bot.message_handler(func=lambda m: True)
def responder(message):
    user_id_str = str(message.from_user.id)
    nome, questao_str, id_questionario = datasheet.get_user_info(user_id_str)

    # Se não existe registro, cria do zero
    if nome is None:
        nome = message.from_user.first_name or "Convidado"
        questao_str = "0"
        id_questionario = ""
        datasheet.update_user_info(user_id=user_id_str, nome=nome, questao=questao_str, id_questionario=id_questionario)

    # Converte questao_str pra int
    questao = int(questao_str) if questao_str else 0

    if questao == 0 or not id_questionario:
        # Não tem questionário em aberto, cria um agora
        # Exemplo: Q<userId>_<timestamp>
        from time import time
        novo_id = f"Q{user_id_str}_{int(time())}"
        questao = 1
        datasheet.update_user_info(user_id=user_id_str,
                                   questao=str(questao),
                                   id_questionario=novo_id)
        bot.reply_to(message, f"Olá, {nome} abrimos um novo questionário para você, ID={novo_id}.\n"
                              f"Responda qualquer coisa para começar.")
        return
    else:
        # Já tem questionário em aberto: a msg do user é a resposta da pergunta 'questao'
        # 1) Gravar na planilha de respostas
        datasheet.update_answer_in_columns(
            id_questionario=id_questionario,
            question_number=questao,
            answer=message.text
        )

        if questao == NUMERO_MAXIMO_QUESTOES:
            # Finalizou
            bot.reply_to(message, "Você respondeu todas as perguntas e elas foram salvas na planilha! Obrigado.")
            datasheet.update_user_info(user_id_str, questao="0", id_questionario="")
        else:
            # Incrementa e pergunta a próxima
            questao += 1
            datasheet.update_user_info(user_id_str, questao=str(questao))
            prox_pergunta = QUESTIONS.get(questao, f"Pergunta {questao} não definida.")
            bot.reply_to(message, prox_pergunta)

def bot_teste():
    bot.polling()
