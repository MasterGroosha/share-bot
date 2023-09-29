# Генерация ссылок «поделиться в Telegram»

На различных веб-сайтах можно встретить кнопку «поделиться в Telegram», позволяющая отправить определённую ссылку 
в (почти) любой чат в мессенджере. Бот, собранный из приведённых в репозитории исходников, 
позволяет генерировать ссылку для такой кнопки.

![пример кнопки «поделиться»](share_button_screenshot.png)

В репозитории вы найдёте два варианта бота; один написан на **Python** при помощи фреймворка [aiogram](https://github.com/aiogram/aiogram). 
Версия для **Golang** использует библиотеку [telebot](https://github.com/tucnak/telebot/).

## Системные требования
**Python**: 3.7+.  
**Go**: при разработке использовалась 1.12.5.  
**ОС**: протестировано в Linux (Manjaro), должно работать и на Windows.

## Systemd

Если в вашей операционной системе есть systemd, то можно настроить автозапуск и удобное управление ботом:

```systemd
[Unit]
Description=Share Helper Bot for Telegram
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/user/share-bot

# Для Golang-версии:
Environment=BOT_TOKEN=токен_бота 
Environment=MODE=polling
ExecStart=/home/user/share-bot/share_bot

# Для Python-версии (используется venv):
# ExecStart=/home/user/share-bot/bin/python /home/user/share-bot/python/polling.py

KillMode=process
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## Deta.Space

Можно загрузить бота на deta.space и получить бесплатный хостинг, поскольку никаких серьёзных действий от бота не требуется. 
Обратите внимание: на связке aiohttp+gunicorn запустить не получится, поэтому приходится тащить fastapi и uvicorn.

Пример `Spacefile`:

```yaml
# Spacefile Docs: https://go.deta.dev/docs/spacefile/v0
v: 0
micros:
  - name: tg-share-bot
    src: python
    run: uvicorn webhook:app
    include:
      - webhook.py
      - handlers.py
      - config_reader.py
      - requirements.txt
    engine: python3.9
    primary: true
    public_routes:
      - "/*"
    presets:
      env:
        - name: BOT_TOKEN
        - name: MODE
          default: "webhook"
        - name: DROP_UPDATES_ON_RESTART
          default: "false"
        - name: WEBHOOK_ADDR
        - name: WEBHOOK_PATH
          default: "/"
        - name: WEBHOOK_SECRET
```

Опробовать бота в деле можно по адресу: https://t.me/tgshare_bot