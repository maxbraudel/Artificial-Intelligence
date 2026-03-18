import logging

from telegram.ext import ApplicationBuilder

import config
from handlers.conversation import conversation_handler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    app.add_handler(conversation_handler)
    logger.info("Bot is running…")
    app.run_polling()


if __name__ == "__main__":
    main()

