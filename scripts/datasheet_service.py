import os
import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

class DataSheetServices:
    def __init__(self):
        """
        Inicializa o serviço de conexão com a planilha do Google,
        lendo as credenciais de variáveis de ambiente.
        """

        # Carrega variáveis do .env (caso ainda não tenha sido carregado)
        load_dotenv()

        self.SCOPES = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        # Monta o dicionário no mesmo formato do JSON de service account:
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

        # Cria as credenciais a partir do dicionário
        self.creds = Credentials.from_service_account_info(service_account_info, scopes=self.SCOPES)

        # Autentica com gspread
        self.client = gspread.authorize(self.creds)

        # Pega o ID da planilha de uma variável de ambiente (ou poderia receber no construtor)
        self.sheet_id = os.environ["SHEET_ID"]
        self.spreadsheet = self.client.open_by_key(self.sheet_id)

        # Define aba padrão
        self.sheet = self.spreadsheet.sheet1

    def get_all_values(self, sheet_name=None):
        """
        Lê todos os valores da aba especificada ou da sheet default (sheet1).
        :param sheet_name: nome da aba (opcional)
        :return: lista de listas contendo os valores
        """
        if sheet_name:
            worksheet = self.spreadsheet.worksheet(sheet_name)
            return worksheet.get_all_values()
        else:
            return self.sheet.get_all_values()

    def append_row(self, row_values, sheet_name=None):
        """
        Adiciona uma nova linha ao final da aba especificada ou da sheet default.
        :param row_values: lista de valores para a nova linha
        :param sheet_name: nome da aba (opcional)
        """
        if sheet_name:
            worksheet = self.spreadsheet.worksheet(sheet_name)
            worksheet.append_row(row_values)
        else:
            self.sheet.append_row(row_values)


# Exemplo de uso isolado:
if __name__ == "__main__":
    # Instancia a classe (ela já lê .env internamente)
    sheet_service = DataSheetServices()

    # Lê todos os valores da aba default
    dados = sheet_service.get_all_values()
    print("Dados lidos:", dados)

    # Escreve uma nova linha na aba default
    #sheet_service.append_row(["Usuário 123", "Resposta X", "Validação OK"])
