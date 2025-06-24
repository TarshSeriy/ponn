import os
import requests
from dotenv import load_dotenv
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Поздравление (с веб-приложением)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton(text="🎉 Открыть сюрприз", web_app=WebAppInfo(url="https://pon-gprfbhkrr-sergeys-projects-f4e91b78.vercel.app/"))],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Я Кубарсыч 🎁\nНажми кнопку, чтобы открыть сюрприз!", reply_markup=reply_markup)

# Котик
async def cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        data = response.json()
        cat_url = data[0]["url"]
        await update.message.reply_photo(cat_url, caption="Вот тебе котик 😻")
    except Exception as e:
        await update.message.reply_text("Что-то пошло не так, котик убежал 😿")

# Бот
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("котик", cat))

app.run_polling()
