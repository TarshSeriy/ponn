import os
import requests
from dotenv import load_dotenv
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CREATOR_ID = int(os.getenv("CREATOR_ID"))  # твой Telegram ID

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🎉 Йоооооооо натискай жоск", web_app=WebAppInfo(url="https://pon-alpha.vercel.app/"))]
    ]
    await update.message.reply_text(
        "З днем народження, красунечко! 🎈 Натискай кнопку — там сюрприз 👀\n\n"
        "А ще напиши *`/cat`* — і отримаєш мили котика 😻\n\n"
        "Сподобалось? Напиши щось (наприклад, *дякую*) — і творець тобі відповість 💌",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode="Markdown"
    )

# /cat — рандомный кот
async def cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        data = response.json()
        cat_url = data[0]["url"]
        await update.message.reply_photo(cat_url, caption="Вот тебе котик 😻")
    except Exception:
        await update.message.reply_text("Что-то пошло не так, котик убежал 😿")

# текстовое сообщение (спасибо и т.п.)
async def handle_thanks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user = update.message.from_user

    msg = (
        f"💌 Сообщение от @{user.username or user.first_name} (ID: {user.id}):\n"
        f"{user_text}\n\n"
        f"Чтобы ответить, используй:\n/ответ {user.id} <текст>"
    )
    await context.bot.send_message(chat_id=CREATOR_ID, text=msg)
    await update.message.reply_text("Спасибо за сообщение! Создатель его увидит и, может быть, ответит ❤️")

# /ответ <user_id> <текст>
async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != CREATOR_ID:
        await update.message.reply_text("⛔ Эту команду может использовать только создатель.")
        return

    try:
        args = context.args
        target_id = int(args[0])
        reply_message = ' '.join(args[1:])
        await context.bot.send_message(chat_id=target_id, text=f"👤 Ответ от создателя:\n{reply_message}")
        await update.message.reply_text("✅ Ответ отправлен!")
    except:
        await update.message.reply_text("⚠️ Неверный формат. Используй:\n/ответ user_id текст")

# запуск бота
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("cat", cat))
app.add_handler(CommandHandler("ответ", reply_to_user))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_thanks))

app.run_polling()
