import logging
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import settings
import sqlite3

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

conn = sqlite3.connect('main.db')
cursor = conn.cursor()
cursor.execute('''
                CREATE TABLE IF NOT EXISTS USERS (
                USER_ID INTEGER PRIMARY KEY NOT NULL, 
                DATE_PAYMENT_END DATE, 
                KEY TEXT REFERENCES KEYS(KEY_ID))
                ''')
cursor.execute('''
                CREATE TABLE IF NOT EXISTS KEYS (
                KEY_ID TEXT PRIMARY KEY,
                USER_ID INTEGER REFERENCES USERS(USER_ID),
                USED BOOLEAN)
                ''')
cursor.execute('''
                CREATE TABLE IF NOT EXISTS KEY_BASE (
                KEY_TOKEN TEXT PRIMARY KEY)
                ''')

cursor.execute('''
                CREATE TABLE IF NOT EXISTS sequence (
                key_id INTEGER PRIMARY KEY AUTOINCREMENT);
                ''')

cursor.execute(''' 
CREATE TRIGGER IF NOT EXISTS after_start AFTER INSERT ON users
FOR EACH ROW
WHEN (new.rowid IS NOT NULL AND new.rowid > 0)
BEGIN
    DELETE FROM sequence;
    INSERT INTO keys (user_id, used, key_id) 
    VALUES (new.rowid, 0, (SELECT key_token FROM key_base 
                           WHERE key_token NOT IN (SELECT key_id FROM sequence) 
                           ORDER BY RANDOM() LIMIT 1));
    INSERT INTO sequence (key_id) 
    VALUES ((SELECT key_token FROM key_base 
            WHERE key_token NOT IN (SELECT key_id FROM sequence) 
            ORDER BY RANDOM() LIMIT 1));
END''')

conn.commit()
conn.close()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

