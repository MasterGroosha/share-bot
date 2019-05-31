# -*- coding: utf-8 -*-

import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
import config
import re
from urllib import parse
from aiogram.utils import exceptions

loop = asyncio.get_event_loop()

bot = Bot(token=config.token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message):
    try:
        await bot.send_message(message.chat.id, config.intro_text, disable_web_page_preview=True, parse_mode="HTML")
    except exceptions.BotBlocked:
        print("Bot was blocked by user, but it's okay now")
        pass



@dp.message_handler(commands=['help'])
async def cmd_help(message):
    try:
        await bot.send_message(message.chat.id, config.help_text, parse_mode="HTML", disable_web_page_preview=True)
    except exceptions.BotBlocked:
        print("Bot was blocked by user, but it's okay now")
        pass


@dp.message_handler(lambda message: True, content_types=['text'])
async def handle_text(message):
    if '|' not in message.text:
        match_result = re.search(config.url_regex, message.text)
        if match_result is None:
            try:
                await bot.send_message(message.chat.id, 'Некорректный URL')
            except exceptions.BotBlocked:
                return
        else:
            external_url = parse.quote(match_result.group())
            try:
                await bot.send_message(message.chat.id, 'Вот ссылка для кнопки \"Поделиться\" (просто скопируйте следующее сообщение):')
                await bot.send_message(message.chat.id, '{!s}{!s}'.format(config.output_base, external_url))
            except exceptions.BotBlocked:
                print("[handle_text] Bot was blocked")
                return
            except Exception as ex:
                print(type(ex), ex)
                return
    else:
        match_result = re.search(config.url_regex, message.text.split('|')[0])
        if match_result is None:
            await bot.send_message(message.chat.id, 'Некорректный URL')
            pass
        else:
            external_url = parse.quote(match_result.group())
            text = parse.quote(message.text.split('|')[1])
            try:
                await bot.send_message(message.chat.id, 'Вот ссылка для кнопки \"Поделиться\" (просто скопируйте следующее сообщение):')
                await bot.send_message(message.chat.id, '{!s}{!s}&text={!s}'.format(config.output_base, external_url, text))
            except Exception as ex:
                print(type(ex), ex)    

    return
    
async def on_startup(app):
    await bot.set_webhook("https://example.com/your_webhook")


if __name__ == '__main__':
    # use skip_updates=True to... well... skip updates :D
    start_webhook(dispatcher=dp, host="127.0.0.1", port=9999, on_startup=on_startup, webhook_path="")
