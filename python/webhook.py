from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import FastAPI

from config_reader import Config, get_config
from handlers import router

config: Config = get_config()

if config.mode == "webhook" and not config.webhook_addr:
    err = "Trying to launch in webhook mode, but no webhook address specified!"
    raise ValueError(err)


app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
bot = Bot(
    config.bot_token.get_secret_value(),
    parse_mode="HTML",
    disable_web_page_preview=True
)
dispatcher = Dispatcher()
dispatcher.include_router(router)


@app.post(config.webhook_path)
async def data_from_telegram(update: Update):
    return await dispatcher.feed_update(bot, update)


@app.on_event("startup")
async def startup_event():
    await bot.delete_webhook(
        drop_pending_updates=config.drop_updates_on_restart
    )
    await bot.set_webhook(
        url=config.webhook_addr + config.webhook_path,
        secret_token=config.webhook_secret.get_secret_value()
    )
