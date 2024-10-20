import asyncio
from create_bot import bot, dp
from start import start_router, register_handlers, set_main_menu


async def main():
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def on_startup():
    register_handlers(dp)
    await set_main_menu(bot)

async def on_shutdown():
    pass


dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)

if __name__ == "__main__":
    asyncio.run(main())
