package main

import (
	"fmt"
	"log"
	"net/url"
	"os"
	"strings"
	"time"

	tb "gopkg.in/tucnak/telebot.v2"
)

const startText string = `
Здравствуйте! Я помогу Вам создать ссылку для кнопки "Поделиться" в Telegram!
Введите ссылку и (опционально) сопровождающий текст в одном из форматов:
1. ССЫЛКА (пример: <code>http://ya.ru</code>).
2. ССЫЛКА|СОПРОВОЖДАЮЩИЙ ТЕКСТ (пример: <code>http://ya.ru|Это Яндекс</code>).

Что это и зачем, можно прочесть <a href="https://t.me/tglive/109">здесь</a>.`

const helpText string = `
Введите ссылку и (опционально) сопровождающий текст в одном из форматов:
1. ССЫЛКА (пример: <code>http://ya.ru</code>).
2. ССЫЛКА|СОПРОВОЖДАЮЩИЙ ТЕКСТ (пример: <code>http://ya.ru|Это Яндекс</code>).

Что это и зачем, можно прочесть <a href="https://t.me/tglive/109">здесь</a>.`

var bot *tb.Bot

func init() {
	var err error
	token := os.Getenv("BOT_TOKEN") // Токен необходимо передавать как переменную окружения
	if len(token) == 0 {
		fmt.Println("Error: No bot token provided. Exiting...")
		os.Exit(1)
	}

	bot, err = tb.NewBot(tb.Settings{
		Token:  token,
		Poller: &tb.LongPoller{Timeout: 10 * time.Second},
	})

	if err != nil {
		log.Fatal(err)
		panic(err)
	}
}

func parseText(message tb.Message, link string) {

	linkQuoted := url.QueryEscape(link)
	var text string
	var resultURL string
	if strings.ContainsAny(message.Text, "|") {
		text = strings.Split(message.Text, "|")[1] // Извлекаем второй токен
		text = strings.Trim(text, " ")             // Убираем пробелы в начале и конце
		text = url.PathEscape(text)                // Экранируем всё
	}

	if len(text) > 0 {
		resultURL = "https://t.me/share/url?url=" + linkQuoted + "&text=" + text
	} else {
		resultURL = "https://t.me/share/url?url=" + linkQuoted
	}

	bot.Send(message.Sender, "Вот ссылка для кнопки \"Поделиться\" (просто скопируйте следующее сообщение):")
	bot.Send(message.Sender, resultURL)
}

func main() {
	// Обработчик всех текстовых сообщений
	bot.Handle(tb.OnText, func(message *tb.Message) {
		if len(message.Entities) > 0 {
			for _, v := range message.Entities {
				if v.Type == tb.EntityURL {
					parseText(*message, message.Text[v.Offset:v.Offset+v.Length])
					break
				}
			}
		} else {
			bot.Reply(message, "URL не найден или некорректен")
		}
	})

	bot.Handle("/start", func(message *tb.Message) {
		bot.Send(message.Sender, startText, &tb.SendOptions{
			ParseMode: tb.ModeHTML,
		})
	})

	bot.Handle("/help", func(m *tb.Message) {
		bot.Send(m.Sender, helpText, &tb.SendOptions{
			ParseMode: tb.ModeHTML,
		})
	})

	bot.Start()
}
