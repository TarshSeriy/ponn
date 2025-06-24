from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os
import requests

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Команда /start — кнопка-сюрприз
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🎉 Йоооооооо нажимай жоск", web_app=WebAppInfo(url="https://pon-alpha.vercel.app/"))]
    ]
    await update.message.reply_text(
        "С днем народження красуня! 🎈 Натискай кнопку, там сюрприз 👀\n\n"
        "А ще напиши *`/cat`* і отримаєш мили котика 😻",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode="Markdown"
    )

# Команда /cat — присылает рандомного кота
async def cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        data = response.json()
        cat_url = data[0]["url"]
        await update.message.reply_photo(cat_url, caption="Вот тебе котик 😻")
    except Exception as e:
        await update.message.reply_text("Что-то пошло не так, котик убежал 😿")

# Запуск бота
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("cat", cat))

app.run_polling()
