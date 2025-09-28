# Digital Door Telegram Bot Service

Bot para Telegram/WhatsApp desenvolvido para melhorar os relatórios de serviços dos funcionários da Digital Door.

## Funcionalidades

- **Cadastro de usuários**: Sistema de registro com validação de nomes
- **Questionário de serviços**: Coleta estruturada de informações sobre serviços realizados
- **Integração Google Sheets**: Armazenamento automático das respostas em planilhas
- **Validação inteligente**: Uso da OpenAI para validar respostas dos usuários
- **Gerenciamento de usuários**: Funcionalidades para adicionar e remover usuários

## Estrutura do Projeto

```
digitaldoor-telegram-bot-service/
├── main.py                    # Arquivo principal
├── requirements.txt           # Dependências do projeto
├── .env.example              # Exemplo de configuração
├── constants/
│   ├── questions.py          # Perguntas do questionário
│   └── validations.py        # Regras de validação
└── scripts/
    ├── bot_telegram.py       # Lógica principal do bot
    ├── datasheet_services.py # Integração com Google Sheets
    └── openai_services.py    # Integração com OpenAI
```

## Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/nandomaki/digitaldoor-telegram-bot-service.git
cd digitaldoor-telegram-bot-service
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

### 4. Configure as credenciais necessárias

#### Telegram Bot
1. Converse com [@BotFather](https://t.me/botfather) no Telegram
2. Crie um novo bot com `/newbot`
3. Copie o token e adicione em `TELEGRAM_API_KEY`

#### OpenAI
1. Acesse [OpenAI Platform](https://platform.openai.com/)
2. Gere uma API key
3. Adicione em `OPENAI_KEY`

#### Google Sheets
1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um projeto e ative a API do Google Sheets
3. Crie uma conta de serviço e baixe o JSON
4. Configure as variáveis `GOOGLE_*` com os dados do JSON
5. Crie duas planilhas no Google Sheets:
   - Uma para controle de usuários (ID em `SHEET_ID`)
   - Uma para respostas do questionário (ID em `SHEET_QUESTIONS`)

## Uso

### Iniciar o bot
```bash
python main.py
```

### Comandos disponíveis

- `/options` - Mostra opções disponíveis
- `/addNewUser` - Cadastra um novo usuário
- `/deleteUser` - Inicia processo de remoção de usuário
- `/sim_excluir` - Confirma remoção do usuário
- `/cancelar` - Cancela operação de remoção

### Fluxo de uso

1. **Cadastro**: Usuário executa `/addNewUser` e informa nome completo
2. **Questionário**: Após cadastro, qualquer mensagem inicia um questionário
3. **Respostas**: Bot faz 7 perguntas sobre o serviço realizado
4. **Armazenamento**: Respostas são salvas automaticamente no Google Sheets

## Questionário de Serviços

O bot coleta as seguintes informações:

1. Em qual cliente foi realizado o serviço?
2. Que horário foi realizado o serviço?
3. Escreva aqui o seu diário de obra dos serviços que foram realizados
4. Qual o horário de chegada no cliente?
5. Qual o horário de saída do cliente?
6. Houve algum problema ou dificuldade durante o serviço? Se sim, descreva
7. Avalie a satisfação do cliente de 1 a 5 (sendo 5 excelente)

## Estrutura das Planilhas

### Planilha de Controle (SHEET_ID)
| id_usuario | Nome | Questao | id_questionario |
|------------|------|---------|-----------------|
| 123456789  | João Silva | 0 | Q123456789_1234567890 |

### Planilha de Respostas (SHEET_QUESTIONS)
| id_questionario | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|-----------------|---|---|---|---|---|---|---|
| Q123456789_1234567890 | Cliente A | 14:00 | Serviço realizado | 13:30 | 16:00 | Nenhum problema | 5 |

## Logs

O bot gera logs em:
- Console (stdout)
- Arquivo `bot.log`

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto é propriedade da Digital Door.

## Suporte

Para suporte técnico, entre em contato com a equipe de desenvolvimento da Digital Door.
