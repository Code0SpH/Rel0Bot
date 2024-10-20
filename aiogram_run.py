import asyncio
from create_bot import bot, dp
from start import start_router, register_handlers, set_main_menu

# from work_time.time_func import send_time_msg

async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def on_startup():
    # Регистрация хэндлеров
    register_handlers(dp)
    await set_main_menu(bot)  # Установка меню для бота

# Закрытие пула соединений при завершении работы бота
async def on_shutdown():
    pass  # Если не нужно ничего закрывать, оставляем пустым

# Регистрация старта и завершения работы бота
dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)

if __name__ == "__main__":
    asyncio.run(main())


