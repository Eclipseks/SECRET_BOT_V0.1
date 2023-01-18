from aiogram import executor

from config import bot, dp
from base.base_db import start_db

import handlers.start_handler


def main():
    executor.start_polling(
        dp, skip_updates = True, on_startup=start_db()
    )


if __name__ == "__main__":
    main()