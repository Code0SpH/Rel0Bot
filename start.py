from aiogram import Router, F, Dispatcher,types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand, LabeledPrice
import sqlite3
import settings
import create_bot

start_router = Router()

prices = [LabeledPrice(label='Доступ к боту', amount=50000)]  # 50000 = 500 рублей

#start
async def process_start(message: types.Message):
    user_id = message.from_user.id
    sql = '''INSERT INTO USERS
             (USER_ID, DATE_PAYMENT_END, KEY)
             VALUES (?, NULL, NULL)
             ON CONFLICT (USER_ID) DO UPDATE
             SET DATE_PAYMENT_END = excluded.                  KEY = excluded.KEY;'''
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute(sql, (user_id,))
    conn.commit()
    conn.close()
    await create_bot.bot.send_message(chat_id=user_id, text='Привет! Вы начали работу с ботом.')

#help
async def process_help_command(message: Message):
    await message.answer('Сообщение из раздела Help')

#support
async def process_support_command(message: Message):
    await message.answer('Контакты разработчиков: @SpH_TVA')

#pay
async def process_pay_command(message: Message):
    try:
        await message.bot.send_invoice(
            chat_id=message.chat.id,
            title='Покупка доступа к боту',
            description='Оплата доступа к боту',
            payload='invoice_payload',  # Убедись, что payload уникален для каждого платежа
            provider_token=settings.PAYMENT_TOKEN,  # Проверка токена в settings
            currency='RUB',
            prices=prices
        )
    except Exception as e:
        await message.answer(f"Произошла ошибка при обработке платежа: {str(e)}")

# Установка команд для главного меню
async def set_main_menu(bot):
    main_menu_commands = [
        BotCommand(command='/start', description='Начало'),
        BotCommand(command='/help', description='Справка по работе бота'),
        BotCommand(command='/support', description='Поддержка'),
        BotCommand(command='/pay', description='Оплата')
    ]
    await bot.set_my_commands(main_menu_commands)

# Функция для регистрации хэндлеров
def register_handlers(dp: Dispatcher):
    dp.message.register(process_start, Command(commands=["start"]))
    dp.message.register(process_help_command, Command(commands=['help']))
    dp.message.register(process_support_command, Command(commands=['support']))
    dp.message.register(process_pay_command, Command(commands=['pay']))
