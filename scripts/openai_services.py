from openai import OpenAI, OpenAIError
import logging

from constants import validations
import config


class OpenAIService:
    """Wrapper around the OpenAI client with simple validation helpers."""

    def __init__(self, api_key: str | None = None):
        self.client = OpenAI(api_key=api_key or config.OPENAI_KEY)

    def validate_answer(self, question_id: int = 1, user_message: str | None = None) -> str:
        """Validate a user answer using OpenAI.

        Returns ``TRUE`` or ``FALSE`` according to predefined rules.
        """
        if question_id == 1:
            rules = validations.QUESTAO_1
        else:
            rules = ""

        prompt = f"""
        {rules}

        Mensagem: '{user_message}'

        Apenas responda `TRUE` ou `FALSE` sem explicações.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um validador de nomes. Responda apenas `TRUE` ou `FALSE`, sem explicações.",
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.8
            )
        except OpenAIError as exc:
            logging.error("OpenAI request failed: %s", exc)
            return "FALSE"

        result = response.choices[0].message.content
        logging.info("Validação resposta: %s", result)
        return result
