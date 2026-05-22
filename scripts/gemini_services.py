import os
from dotenv import load_dotenv
import google.generativeai as genai
from constants import validations


class GeminiServices:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY não encontrada nas variáveis de ambiente")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-pro",
            system_instruction="Você é um validador de respostas. Responda apenas TRUE ou FALSE, sem explicações.",
            generation_config=genai.types.GenerationConfig(
                temperature=0.1,
                max_output_tokens=10,
            ),
        )

    def validarResposta(self, id_question=1, user_message=None):
        if not user_message:
            return "FALSE"

        try:
            if id_question == 1:
                regras = validations.QUESTAO_1
            else:
                regras = "Valide se a resposta está adequada."

            prompt = f"{regras}\n\nMensagem: '{user_message}'\n\nApenas responda TRUE ou FALSE sem explicações."

            response = self.model.generate_content(prompt)
            resultado = response.text.strip().upper()

            if resultado in ["TRUE", "FALSE"]:
                return resultado
            return "FALSE"

        except Exception as e:
            print(f"Erro na validação Gemini: {e}")
            return "FALSE"
