from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context):
    keyboard = [
        [KeyboardButton("🎉 Открыть поздравление", web_app=WebAppInfo(url="https://pon-alpha.vercel.app/"))]
    ]
    await update.message.reply_text(
        "С днюшкой твоей подруг! Жми кнопку 🎈",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
