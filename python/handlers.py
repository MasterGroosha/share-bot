import re
from urllib import parse

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()

url_regex = r"[Hh]ttp[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
regex = re.compile(url_regex)


@router.message(CommandStart())
async def start(message: Message):
    intro_text = "Здравствуйте! Я помогу Вам создать ссылку для кнопки \"Поделиться\" в Telegram\n" \
                 "Пожалуйста, введите ссылку и (опционально) сопровождающий текст в одном из форматов:\n" \
                 "1. ССЫЛКА (пример: <code>http://ya.ru</code>).\n" \
                 "2. ССЫЛКА|СОПРОВОЖДАЮЩИЙ ТЕКСТ (пример: <code>http://ya.ru|Это Яндекс</code>).\n\n" \
                 "Что это и зачем, можно прочесть <a href=\"https://t.me/tglive/109\">здесь</a>."
    await message.answer(intro_text)


@router.message(Command("help"))
async def cmd_help(message: Message):
    help_text = "Введите ссылку и (опционально) сопровождающий текст в одном из форматов:\n" \
                "1. ССЫЛКА (пример: <code>http://ya.ru</code>).\n" \
                "2. ССЫЛКА|СОПРОВОЖДАЮЩИЙ ТЕКСТ (пример: <code>http://ya.ru|Это Яндекс</code>).\n\n" \
                "Что это и зачем, можно прочесть <a href=\"https://t.me/tglive/109\">здесь</a>."
    await message.answer(help_text)


@router.message()
async def handle_text(message: Message):
    output_base = 'https://t.me/share/url?url='

    if '|' not in message.text:
        match_result = re.search(regex, message.text)
        if match_result is None:
            await message.answer('Некорректный URL')
        else:
            external_url = parse.quote(match_result.group())
            await message.answer('Вот ссылка для кнопки "Поделиться" (просто скопируйте следующее сообщение):')
            await message.answer(f'{output_base}{external_url}', parse_mode=None)

    else:
        match_result = re.search(url_regex, message.text.split('|')[0])
        if match_result is None:
            await message.answer('Некорректный URL')
        else:
            external_url = parse.quote(match_result.group())
            text = parse.quote(message.text.split('|')[1])
            await message.answer('Вот ссылка для кнопки \"Поделиться\" (просто скопируйте следующее сообщение):')
            await message.answer(f'{output_base}{external_url}&text={text}', parse_mode=None)
