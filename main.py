"""
Digital Door Telegram Bot Service
Bot para Telegram/WhatsApp para melhorar relatórios de serviços de funcionários.
"""

import sys
import logging
from scripts import bot_telegram

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    """
    Função principal que inicia o bot do Telegram.
    """
    try:
        logger.info("Iniciando Digital Door Telegram Bot Service...")
        bot_telegram.bot_teste()
    except KeyboardInterrupt:
        logger.info("Bot interrompido pelo usuário.")
    except Exception as e:
        logger.error(f"Erro crítico no bot: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
