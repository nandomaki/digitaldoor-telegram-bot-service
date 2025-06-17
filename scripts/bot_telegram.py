import telebot
import os
from dotenv import load_dotenv
from scripts.datasheet_services import DataSheetServices
from scripts.openai_services import OpenAIServices
from constants.questions import QUESTIONS, NUMERO_MAXIMO_QUESTOES

load_dotenv()
CHAVE_API = os.getenv("TELEGRAM_API_KEY")
bot = telebot.TeleBot(CHAVE_API)

datasheet = DataSheetServices()
openai_services = OpenAIServices()


################ FUNÇÔES DE CONTROLE DE USUÀRIOS ################

@bot.message_handler(commands=['options'])
def options(message):
    text = """
    Escolha as opções que deseja fazer:

        1 - /addNewUser para adicionar um novo usuário
        2 - /deleteUser para deletar um usuário
    
    Clique na opção desejada.
    """
    bot.reply_to(message, text)


################ FUNÇÔES DE CADICIONAR NOVO USUÁRIOS ################

@bot.message_handler(commands=['addNewUser'])
def add_new_user(message):
    user_id_str = str(message.from_user.id)
    user_existe = datasheet.user_exists(user_id_str)

    if not user_existe:
        # Não existe registro para esse ID; cria com nome=None, questao=-99
        datasheet.update_user_info(
            user_id=user_id_str,
            nome="",  # Representando None
            questao="-99",  # Significa "aguardando nome"
            id_questionario=""  # Representando None
        )
        text = (f"Novo usuário criado com ID={user_id_str}, "
                f"nome=None, questao=-99, id_questionario=None.\n"
                f"Por favor, envie seu nome completo agora.")
    else:
        # Já existe, mostra as informações
        nome, questao_str, id_questionario = datasheet.get_user_info(user_id_str)
        if nome is None or nome == "":
            text = (f"Usuário com ID={user_id_str} já está cadastrado sem nome. "
                    "Envie seu nome completo agora para finalizar o cadastro.")
        else:
            text = (f"Usuário com ID={user_id_str} já está cadastrado com o nome: {nome}.\n"
                    "Se precisar editar, fale com o administrador.")

    bot.reply_to(message, text)


################ FUNÇÔES DE PRINCIPAL# FUNÇÔES DE REMOÇÃO DE USUARIOS ################

@bot.message_handler(commands=['deleteUser'])
def deleteUser(message):
    text = """
    "Você realmente deseja apagar seu usuário? (O histórico de serviços não será exluído!)
        /sim_excluir se deseja a exclusão
        /cancelar para cancelar este comando
    """
    bot.send_message(message.chat.id,text)


@bot.message_handler(commands=['cancelar'])
def cancelar(message):
    bot.send_message(message.chat.id, "Operação cancelada!")


@bot.message_handler(commands=['sim_excluir'])
def sim_excluir(message):

    user_id_str = str(message.from_user.id)
    user_existe = datasheet.user_exists(user_id_str)
    if user_existe:
        was_removed = datasheet.remove_user_info(user_id_str)
        if was_removed:
            bot.send_message(message.chat.id, "Você foi removido com sucesso!")
        else:
            bot.send_message(message.chat.id, "Não foi possível sua remoção.")
    else:
        bot.send_message(message.chat.id, "Você não está cadastrado! Digite /options para cadastrar.")


############### FUNÇÔES DE PRINCIPAL ################

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    """Handler genérico para TODAS as mensagens que não sejam comandos.
       Se questao_str == '-99', valida nome.
       Caso contrário, segue o fluxo do questionário normal.
    """
    user_id_str = str(message.from_user.id)

    user_existe = datasheet.user_exists(user_id_str)
    if user_existe:
        nome, questao_str, id_questionario = datasheet.get_user_info(user_id_str)

        # Se o usuário foi criado com questao=-99, quer dizer que estamos aguardando nome
        if questao_str == '-99':
            # Valida nome usando OpenAI
            nome_valido = openai_services.validarResposta(1, message.text)

            if nome_valido.strip().upper() == 'TRUE':
                # Atualiza o cadastro para questao=0 e insere o nome
                datasheet.update_user_info(
                    user_id=user_id_str,
                    nome=message.text,
                    questao="0",
                    id_questionario=""
                )
                bot.reply_to(message, "Nome salvo com sucesso! Agora você pode iniciar um questionário.")
            else:
                bot.reply_to(message, "Nome inválido. Favor informar nome e sobrenome.")
            return  # Não continua o fluxo de questionário

        # Se não estamos aguardando nome, vamos para o fluxo de questionário
        questao = int(questao_str) if questao_str else 0

        if questao == 0 or not id_questionario:
            # Não tem questionário em aberto, cria um novo
            from time import time
            novo_id = f"Q{user_id_str}_{int(time())}"
            questao = 1

            datasheet.update_user_info(
                user_id=user_id_str,
                questao=str(questao),
                id_questionario=novo_id
            )
            bot.reply_to(message, f"Olá, {nome or 'Usuário'}! Abrimos um novo questionário para você, ID={novo_id}.\n"
                                  f"Responda qualquer coisa para começar.")
        else:
            # Já tem questionário em aberto: a mensagem do user é a resposta da pergunta 'questao'
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
    else:
        bot.send_message(
            message.chat.id,
            "Você não está cadastrado, favor Cadastre-se. Digite /options para abrir a tela de opções."
        )


def bot_teste():
    bot.polling()
