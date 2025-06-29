import gspread
from google.oauth2.service_account import Credentials
import logging

import config


class DataSheetServices:
    def __init__(self, client: gspread.Client | None = None):
        """
        Inicializa a conexão com DUAS planilhas separadas:
          - Planilha de controle (SHEET_ID)
          - Planilha de respostas (SHEET_QUESTIONS)
        Lendo as credenciais de variáveis de ambiente.
        """

        # Credentials and sheet IDs are loaded from config

        self.SCOPES = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        service_account_info = {
            "type": "service_account",
            "project_id": config.GOOGLE_PROJECT_ID,
            "private_key_id": config.GOOGLE_PRIVATE_KEY_ID,
            "private_key": (config.GOOGLE_PRIVATE_KEY or "").replace("\\n", "\n"),
            "client_email": config.GOOGLE_CLIENT_EMAIL,
            "client_id": config.GOOGLE_CLIENT_ID,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": (
                "https://www.googleapis.com/robot/v1/metadata/x509/"
                + (config.GOOGLE_CLIENT_EMAIL or "").replace("@", "%40")
            )
        }

        self.creds = Credentials.from_service_account_info(service_account_info, scopes=self.SCOPES)
        self.client = client or gspread.authorize(self.creds)

        # IDs de cada planilha definidos nas variáveis de ambiente
        self.sheet_id_control = config.SHEET_ID
        self.sheet_id_questions = config.SHEET_QUESTIONS

        # Abre cada planilha
        try:
            self.spreadsheet_control = self.client.open_by_key(self.sheet_id_control)
            self.spreadsheet_questions = self.client.open_by_key(self.sheet_id_questions)
        except Exception as exc:
            logging.error("Erro abrindo planilhas: %s", exc)
            raise

        # Define aba padrão para cada uma (sheet1, por exemplo)
        self.sheet_control = self.spreadsheet_control.sheet1
        self.sheet_questions = self.spreadsheet_questions.sheet1

    # -------------------------- Método genérico get_all_values --------------------------
    def get_all_values(self, planilha: str = "control", sheet_name: str = None):
        """
        Lê todos os valores de uma determinada planilha (control ou questions).
        :param planilha: "control" para planilha de controle, "questions" para planilha de respostas.
        :param sheet_name: opcional, nome da aba. Se None, usa a aba padrão (sheet1).
        :return: lista de listas contendo os valores
        """
        if planilha == "control":
            ws = (
                self.spreadsheet_control.worksheet(sheet_name)
                if sheet_name
                else self.sheet_control
            )
        elif planilha == "questions":
            ws = (
                self.spreadsheet_questions.worksheet(sheet_name)
                if sheet_name
                else self.sheet_questions
            )
        else:
            raise ValueError("Parâmetro 'planilha' inválido. Use 'control' ou 'questions'.")

        return ws.get_all_values()

    # ---------------- Planilha de CONTROLE (SHEET_ID) ----------------

    def get_user_info(self, user_id: str, sheet_name=None):
        """
        Retorna (nome, questao, id_questionario) do user_id na planilha de controle.
        Se não achar, retorna (None, None, None).
        Esperamos no cabeçalho: [id_usuario, Nome, Questao, id_questionario]
        """
        data = self.get_all_values(planilha="control", sheet_name=sheet_name)
        if not data:
            return (None, None, None)

        # data[0] é o cabeçalho
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
        """Create or update a user row in the control spreadsheet."""
        ws = self.spreadsheet_control.worksheet(sheet_name) if sheet_name else self.sheet_control

        try:
            cell = ws.find(user_id)
        except Exception:
            cell = None

        if cell:
            row_index = cell.row
            row = ws.row_values(row_index)
            while len(row) < 4:
                row.append("")
            if nome is not None:
                row[1] = nome
            if questao is not None:
                row[2] = questao
            if id_questionario is not None:
                row[3] = id_questionario
            ws.update(f"A{row_index}:D{row_index}", [row[:4]])
        else:
            new_row = [user_id, nome or "", questao or "0", id_questionario or ""]
            ws.append_row(new_row)

    def user_exists(self, user_id: str, sheet_name=None) -> bool:
        """
        Retorna True se user_id existe na planilha de controle, False se não existe.
        """
        data = self.get_all_values(planilha="control", sheet_name=sheet_name)
        if len(data) < 2:
            return False  # só cabeçalho ou nada

        # pula o cabeçalho data[0]
        for row in data[1:]:
            if row and row[0] == user_id:
                return True
        return False

    # ---------------- Planilha de RESPOSTAS (SHEET_QUESTIONS) ----------------

    def update_answer_in_columns(self, id_questionario: str, question_number: int, answer: str, sheet_name=None):
        """
        Atualiza a planilha de respostas para que:
          - A coluna 'question_number' no cabeçalho (strings "1","2","3", etc.)
          - A linha com id_questionario == row[0]
        receba 'answer'.
        Exemplo de cabeçalho:
        [id_questionario, "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
        """
        ws = self.spreadsheet_questions.worksheet(sheet_name) if sheet_name else self.sheet_questions

        try:
            header = ws.row_values(1)
        except Exception:
            header = []

        if not header:
            header = ["id_questionario"] + [str(i) for i in range(1, 21)]
            ws.insert_row(header, 1)

        if question_number >= len(header):
            raise ValueError(f"Não há coluna para a pergunta #{question_number}. Verifique o cabeçalho.")

        try:
            cell = ws.find(id_questionario)
        except Exception:
            cell = None

        if cell:
            row_index = cell.row
            ws.update_cell(row_index, question_number + 1, answer)
        else:
            new_row = ["" for _ in header]
            new_row[0] = id_questionario
            new_row[question_number] = answer
            ws.append_row(new_row)

    def remove_user_info(self, user_id: str, sheet_name=None) -> bool:
        """
        Remove a linha que contém 'user_id' na primeira coluna (id_usuario).
        Retorna True se encontrou e removeu, ou False se não encontrou.
        """
        # Acessa a aba da planilha de controle
        ws = self.spreadsheet_control.worksheet(sheet_name) if sheet_name else self.sheet_control
        data = ws.get_all_values()

        # Se a planilha estiver vazia ou só com cabeçalho, não há o que remover
        if len(data) < 2:
            return False

        header = data[0]
        new_data = [header]  # Manter o cabeçalho na nova lista
        removed = False

        # Percorre as linhas, pulando o cabeçalho (data[1:])
        for row in data[1:]:
            # row[0] é o 'id_usuario'
            if row and row[0] == user_id:
                removed = True  # Encontrou o usuário, não adiciona a 'new_data'
            else:
                new_data.append(row)

        # Se encontrou e removeu, atualiza a planilha
        if removed:
            ws.clear()
            ws.update("A1", new_data)

        return removed

