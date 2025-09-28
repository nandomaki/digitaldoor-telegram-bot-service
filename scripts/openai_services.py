import os
from dotenv import load_dotenv
from openai import OpenAI
from constants import validations


class OpenAIServices:
    def __init__(self):
        """
        Inicializa o cliente OpenAI com a nova API.
        """
        load_dotenv()
        api_key = os.getenv("OPENAI_KEY")
        
        if not api_key:
            raise ValueError("OPENAI_KEY não encontrada nas variáveis de ambiente")
        
        self.client = OpenAI(api_key=api_key)

    def validarResposta(self, id_question=1, user_message=None):
        """
        Valida a resposta do usuário usando OpenAI.
        
        Args:
            id_question (int): ID da questão a ser validada
            user_message (str): Mensagem do usuário para validação
            
        Returns:
            str: "TRUE" ou "FALSE" baseado na validação
        """
        if not user_message:
            return "FALSE"
        
        try:
            # Seleciona as regras baseadas na questão
            if id_question == 1:
                regras = validations.QUESTAO_1
            else:
                # Para futuras questões, pode expandir aqui
                regras = "Valide se a resposta está adequada."

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
                        "content": "Você é um validador de respostas. Responda apenas `TRUE` ou `FALSE`, sem explicações."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=10,  # Reduzido já que esperamos apenas TRUE/FALSE
                temperature=0.1  # Reduzido para respostas mais consistentes
            )

            resultado = response.choices[0].message.content.strip().upper()
            
            # Garante que retorna apenas TRUE ou FALSE
            if resultado in ["TRUE", "FALSE"]:
                return resultado
            else:
                # Se a resposta for inesperada, assume FALSE por segurança
                return "FALSE"
                
        except Exception as e:
            print(f"Erro na validação OpenAI: {e}")
            # Em caso de erro, assume FALSE por segurança
            return "FALSE"
