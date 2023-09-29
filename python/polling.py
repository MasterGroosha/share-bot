import asyncio

from aiogram import Bot, Dispatcher

from config_reader import Config, get_config
from handlers import router


async def main():
    config: Config = get_config()

    bot = Bot(
        config.bot_token.get_secret_value(),
        parse_mode="HTML",
        disable_web_page_preview=True
    )
    dispatcher = Dispatcher()
    dispatcher.include_router(router)

    await bot.delete_webhook(
        drop_pending_updates=config.drop_updates_on_restart
    )
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
