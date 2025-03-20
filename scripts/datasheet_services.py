import os
import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

class DataSheetServices:
    def __init__(self):
        """
        Inicializa a conexão com DUAS planilhas separadas:
          - Planilha de controle (SHEET_ID)
          - Planilha de respostas (SHEET_QUESTIONS)
        Lendo as credenciais de variáveis de ambiente.
        """

        load_dotenv()

        self.SCOPES = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        service_account_info = {
            "type": "service_account",
            "project_id": os.environ["GOOGLE_PROJECT_ID"],
            "private_key_id": os.environ["GOOGLE_PRIVATE_KEY_ID"],
            "private_key": os.environ["GOOGLE_PRIVATE_KEY"].replace("\\n", "\n"),
            "client_email": os.environ["GOOGLE_CLIENT_EMAIL"],
            "client_id": os.environ["GOOGLE_CLIENT_ID"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": (
                "https://www.googleapis.com/robot/v1/metadata/x509/"
                + os.environ["GOOGLE_CLIENT_EMAIL"].replace("@", "%40")
            )
        }

        self.creds = Credentials.from_service_account_info(service_account_info, scopes=self.SCOPES)
        self.client = gspread.authorize(self.creds)

        # IDs de cada planilha no .env
        self.sheet_id_control = os.environ["SHEET_ID"]
        self.sheet_id_questions = os.environ["SHEET_QUESTIONS"]

        # Abre cada planilha
        self.spreadsheet_control = self.client.open_by_key(self.sheet_id_control)
        self.spreadsheet_questions = self.client.open_by_key(self.sheet_id_questions)

        # Define aba padrão para cada uma (sheet1, por exemplo)
        self.sheet_control = self.spreadsheet_control.sheet1
        self.sheet_questions = self.spreadsheet_questions.sheet1

    # ---------------- Planilha de CONTROLE (SHEET_ID) ----------------

    def get_all_values_control(self, sheet_name=None):
        """Retorna todas as linhas da planilha de controle."""
        if sheet_name:
            ws = self.spreadsheet_control.worksheet(sheet_name)
            return ws.get_all_values()
        else:
            return self.sheet_control.get_all_values()

    def get_user_info(self, user_id: str, sheet_name=None):
        """
        Retorna (nome, questao, id_questionario) do user_id.
        Se não achar, retorna (None, None, None).
        Cabeçalho esperado: [id_usuario, Nome, Questao, id_questionario]
        """
        data = self.get_all_values_control(sheet_name)
        if not data:
            return (None, None, None)

        for row in data[1:]:
            if row and len(row) >= 4:
                # row[0] = id_usuario
                # row[1] = Nome
                # row[2] = Questao
                # row[3] = id_questionario
                if row[0] == user_id:
                    return (row[1], row[2], row[3])
        return (None, None, None)

    def update_user_info(self, user_id: str, nome=None, questao=None, id_questionario=None, sheet_name=None):
        """
        Atualiza/cria a linha do user_id na planilha de controle.
        Se não existir, cria. Sobrescreve a planilha inteira.
        (Para simplificar; em produção, você pode fazer algo mais incremental)
        """
        ws = self.spreadsheet_control.worksheet(sheet_name) if sheet_name else self.sheet_control
        data = ws.get_all_values()

        if not data:
            data = [["id_usuario", "Nome", "Questao", "id_questionario"]]

        header = data[0]
        found = False
        for i, row in enumerate(data[1:], start=1):
            if len(row) >= 1 and row[0] == user_id:
                # Atualiza
                if nome is not None:
                    row[1] = nome
                if questao is not None:
                    row[2] = questao
                if id_questionario is not None:
                    row[3] = id_questionario
                data[i] = row
                found = True
                break

        if not found:
            # Cria nova linha
            new_row = [
                user_id,
                nome or "",
                questao or "0",
                id_questionario or ""
            ]
            data.append(new_row)

        # Regrava a planilha
        ws.clear()
        ws.update("A1", data)

    # ---------------- Planilha de RESPOSTAS (SHEET_QUESTIONS) ----------------

    def get_all_values_questions(self, sheet_name=None):
        """Retorna todas as linhas da planilha de respostas."""
        if sheet_name:
            ws = self.spreadsheet_questions.worksheet(sheet_name)
            return ws.get_all_values()
        else:
            return self.sheet_questions.get_all_values()

    def update_answer_in_columns(self, id_questionario: str, question_number: int, answer: str, sheet_name=None):
        """
        Atualiza a planilha de respostas para que:
          - A coluna 'question_number' (que deve existir no cabeçalho: '1','2','3', etc.)
          - A linha com id_questionario == row[0]
        receba o 'answer'.

        Exemplo de cabeçalho:
        [id_questionario, "1", "2", "3", "4", "5", "6", "7"]
        """
        ws = self.spreadsheet_questions.worksheet(sheet_name) if sheet_name else self.sheet_questions
        data = ws.get_all_values()
        if not data:
            # Cria cabeçalho mínimo: 8 colunas (7 perguntas + id_questionario)
            data = [["id_questionario", "1", "2", "3", "4", "5", "6", "7"]]

        header = data[0]

        # A primeira coluna (col 0) é id_questionario, as seguintes correspondem às perguntas
        # question_number=1 -> header[1]
        # question_number=2 -> header[2], etc.
        if question_number >= len(header):
            raise ValueError(f"Não há coluna para a pergunta #{question_number}. Verifique seu cabeçalho.")

        # Procura a linha do id_questionario
        found = False
        for i, row in enumerate(data[1:], start=1):
            if row and row[0] == id_questionario:
                # Garante que a linha tenha tamanho suficiente
                while len(row) < len(header):
                    row.append("")
                row[question_number] = answer
                data[i] = row
                found = True
                break

        if not found:
            # Cria nova linha
            new_row = ["" for _ in header]
            new_row[0] = id_questionario
            new_row[question_number] = answer
            data.append(new_row)

        # Sobrescreve a planilha
        ws.clear()
        ws.update("A1", data)
