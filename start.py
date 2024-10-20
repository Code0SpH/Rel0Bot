from aiogram import Router, F, Dispatcher,types
from aiogram.filters import Command
from aiogram.types import Message, BotCommand, LabeledPrice, PreCheckoutQuery
import sqlite3
import settings
import create_bot

start_router = Router()

prices = [LabeledPrice(label='Доступ к ключу', amount=50000)]

#start
async def process_start(message: types.Message):
    user_id = message.from_user.id
    sql = '''INSERT INTO USERS
             (USER_ID, DATE_PAYMENT_END, KEY)
             VALUES (?, NULL, NULL)
             ON CONFLICT (USER_ID) DO UPDATE
             SET DATE_PAYMENT_END = excluded.KEY = excluded.KEY;'''
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute(sql, (user_id,))
    conn.commit()
    conn.close()
    await create_bot.bot.send_message(chat_id=user_id, text='Привет, я Бот, который поможет тебе купить ключ от игры.')

#help
async def process_help_command(message: Message):
    await message.answer('Сообщение из раздела Help')

#support
async def process_support_command(message: Message):
    await message.answer('Контакты разработчика - @SpH_TVA')

#pay
async def process_pay_command(message: Message):
    try:
        await message.bot.send_invoice(
            chat_id=message.chat.id,
            title='Покупка доступа к игре',
            description='Оплата доступа к игре',
            payload='invoice_payload_' + str(message.from_user.id),
            provider_token=settings.PAYMENT_TOKEN,
            currency='RUB',
            prices=prices,
            start_parameter='start',
            is_flexible=False
        )
    except Exception as e:
        await message.answer(f"Произошла ошибка при обработке платежа: {str(e)}")

# Обработка подтверждения перед оплатой
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await pre_checkout_q.answer(ok=True)

# Обработка успешной оплаты
async def got_payment(message: Message):
    successful_payment = message.successful_payment
    await message.answer(f"Спасибо за оплату! Вы успешно приобрели {successful_payment.total_amount / 100} {successful_payment.currency}.")
    # Здесь можно добавить логику предоставления доступа к платному функционалу


async def set_main_menu(bot):
    main_menu_commands = [
        BotCommand(command='/start', description='Начало'),
        BotCommand(command='/help', description='Справка по работе бота'),
        BotCommand(command='/support', description='Поддержка'),
        BotCommand(command='/pay', description='Оплата')
    ]
    await bot.set_my_commands(main_menu_commands)

def register_handlers(dp: Dispatcher):
    dp.message.register(process_start, Command(commands=["start"]))
    dp.message.register(process_help_command, Command(commands=['help']))
    dp.message.register(process_support_command, Command(commands=['support']))
    dp.message.register(process_pay_command, Command(commands=['pay']))
    dp.message.register(got_payment, Command(commands=["successful_payment"]))
    dp.pre_checkout_query.register(pre_checkout_query)