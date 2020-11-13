import re
from urllib import parse
from sys import exit
from os import getenv
from aiogram import Bot, types, executor
from aiogram.dispatcher import Dispatcher
from aiogram.utils import exceptions
import config


token = getenv("BOT_TOKEN")
if not token:
    exit("No token provided!")

bot = Bot(token=token)
dp = Dispatcher(bot)
regex = re.compile(config.url_regex)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(config.intro_text, disable_web_page_preview=True, parse_mode="HTML")


@dp.message_handler(commands='help')
async def cmd_help(message: types.Message):
    await message.answer(config.help_text, disable_web_page_preview=True, parse_mode="HTML")


@dp.message_handler()
async def handle_text(message: types.Message):
    if '|' not in message.text:
        match_result = re.search(regex, message.text)
        if match_result is None:
            await message.answer('Некорректный URL')
        else:
            external_url = parse.quote(match_result.group())
            await message.answer('Вот ссылка для кнопки "Поделиться" (просто скопируйте следующее сообщение):')
            await message.answer(f'{config.output_base}{external_url}')

    else:
        match_result = re.search(config.url_regex, message.text.split('|')[0])
        if match_result is None:
            await message.answer('Некорректный URL')
        else:
            external_url = parse.quote(match_result.group())
            text = parse.quote(message.text.split('|')[1])
            await message.answer('Вот ссылка для кнопки \"Поделиться\" (просто скопируйте следующее сообщение):')
            await message.answer(f'{config.output_base}{external_url}&text={text}')


@dp.errors_handler(exception=exceptions.BotBlocked)
async def bot_blocked_exception(update, error):
    # Если бот заблокирован, ничего не делаем
    return True


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
