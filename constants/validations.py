"""
Constantes de validação para o bot do Telegram.
Contém as regras de validação para cada questão do questionário.
"""

QUESTAO_1 = """
Você está sendo utilizado para validar respostas de usuário em um chatbot de Telegram, 
para verificar se a resposta está de acordo com o esperado antes de prosseguir para a próxima etapa.

Esta é a primeira pergunta a ser validada:  
O usuário deve informar seu nome completo seguindo estas regras:

1 - O nome precisa conter pelo menos um primeiro nome e um sobrenome.  
   - Exemplos válidos: "João da Costa", "Maria Pereira", "Luiz Coppini", "Ana Souza Silva".  
   - Exemplos inválidos: "João", "Maria", "Luiz", "Ana".  

Responda **apenas** com `TRUE` ou `FALSE`, sem explicações adicionais.  
Se o nome for válido, retorne `TRUE`. Caso contrário, retorne `FALSE`.  
"""

QUESTAO_2 = """
Valide se o usuário informou um horário válido para o serviço.
O horário deve estar no formato HH:MM ou similar (ex: 14:30, 9:00, 16h30).
Aceite formatos flexíveis mas que representem um horário válido.

Exemplos válidos: "14:30", "9:00", "16h30", "8:15", "das 9 às 17"
Exemplos inválidos: "ontem", "cedo", "tarde", "xxx"

Responda apenas `TRUE` ou `FALSE`.
"""

QUESTAO_3 = """
Valide se o usuário forneceu uma descrição adequada do diário de obra.
A resposta deve conter pelo menos 10 caracteres e descrever atividades realizadas.

Exemplos válidos: "Instalação de equipamentos", "Manutenção preventiva realizada"
Exemplos inválidos: "ok", "sim", "nada", "xxx"

Responda apenas `TRUE` ou `FALSE`.
"""

QUESTAO_4 = """
Valide se o usuário informou um horário válido de chegada.
O horário deve estar no formato HH:MM ou similar.

Exemplos válidos: "13:30", "8:00", "14h15"
Exemplos inválidos: "cedo", "tarde", "não lembro"

Responda apenas `TRUE` ou `FALSE`.
"""

QUESTAO_5 = """
Valide se o usuário informou um horário válido de saída.
O horário deve estar no formato HH:MM ou similar.

Exemplos válidos: "17:30", "16:00", "18h45"
Exemplos inválidos: "tarde", "depois", "não sei"

Responda apenas `TRUE` ou `FALSE`.
"""

QUESTAO_6 = """
Valide se o usuário forneceu uma resposta sobre problemas ou dificuldades.
Aceite tanto "não houve problemas" quanto descrições de problemas específicos.
A resposta deve ter pelo menos 3 caracteres.

Exemplos válidos: "Nenhum problema", "Dificuldade de acesso", "Não"
Exemplos inválidos: "x", "ok", ""

Responda apenas `TRUE` ou `FALSE`.
"""

QUESTAO_7 = """
Valide se o usuário forneceu uma avaliação de satisfação válida.
Deve ser um número de 1 a 5 ou texto equivalente.

Exemplos válidos: "5", "4", "3", "excelente", "bom", "regular"
Exemplos inválidos: "6", "0", "ruim demais", "xxx"

Responda apenas `TRUE` ou `FALSE`.
"""
