from openai import OpenAI
import os
from dotenv import load_dotenv
from constants import validations

class OpenAIServices:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

    def validarResposta(self, id_question=1, user_message=None):
        if id_question == 1:
            regras = validations.QUESTAO_1
        prompt = f"""
        {regras}

        Mensagem: '{user_message}'

        Apenas responda `TRUE` ou `FALSE` sem explicações.
        """

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um validador de nomes. Responda apenas `TRUE` ou `FALSE`, sem explicações."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.8
        )

        valido = response.choices[0].message.content

        print(valido)
        return valido
