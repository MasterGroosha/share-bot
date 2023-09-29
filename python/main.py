import asyncio

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config_reader import Config, get_config
from handlers import router


async def main():
    config: Config = get_config()
    if config.mode != "polling" and not config.webhook_addr:
        err = "Trying to launch in webhook mode, but no webhook address specified!"
        raise ValueError(err)

    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML", disable_web_page_preview=True)
    dispatcher = Dispatcher()
    dispatcher.include_router(router)

    await bot.delete_webhook(drop_pending_updates=config.drop_updates_on_restart)

    if config.mode == "polling":
        await dispatcher.start_polling(bot)
    else:
        app = web.Application()
        webhook_handler = SimpleRequestHandler(
            dispatcher=dispatcher,
            bot=bot,
            secret_token=config.webhook_secret.get_secret_value()
        )
        webhook_handler.register(app, path=config.webhook_path)
        setup_application(app, dispatcher, bot=bot)
        await bot.set_webhook(
            url=config.webhook_addr + config.webhook_path,
            secret_token=config.webhook_secret.get_secret_value()
        )
        return app


if __name__ == '__main__':
    asyncio.run(main())
