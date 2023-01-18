from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

API = '5858959660:AAFinD9qhetpy6EstQwsqbk-5GQVo5SgHLc'
CHECK_GROUP = -1001816923180
# CHECK_GROUP = -1001824836801
APPROVE_PHOTO = 'AgACAgIAAxkBAAICy2O6vLJ69MbIg-cK7jQO_5c3VyToAAKpwzEbXBzRSVj33J71ZPrBAQADAgADeQADLQQ'


bot = Bot(token=API, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
