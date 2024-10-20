import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import settings
import sqlite3


scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

conn = sqlite3.connect('main.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS USERS
            	(id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
conn.close()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())


