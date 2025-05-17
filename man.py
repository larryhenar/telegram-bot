from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from urllib.parse import quote_plus
from flask import Flask
import threading

TOKEN = "7981464517:AAEjVIuHT9YEV__yIqXubzXhaEdYsJwBHsc"
CHANNEL_LINK = "https://t.me/+uTWZMQSqTYFiYjE1"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    encoded_link = quote_plus(CHANNEL_LINK)
    keyboard = [
        [InlineKeyboardButton("🔗 Share to 1 Group [0/1]🔑", url=f"https://t.me/share/url?url={encoded_link}")],
        [InlineKeyboardButton("🔗 Share to 2 People [0/2]🔑", url=f"https://t.me/share/url?url={encoded_link}")],
        [InlineKeyboardButton("✅ Unlock", callback_data="unlock")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "To unlock premium content, complete the task below👇:\n\n"
        "✅ Share the link with 1 Group and 2 People.\n\n"
        "Then click ✅ Unlock.",
        reply_markup=reply_markup
    )

async def unlock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("✅ Looks like you didn't complete the task. Type /start to start again.")

async def reply_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='You will be let in only when you share in one group and two people. Type "/start" and try again!'
    )

def main():
    threading.Thread(target=run_flask).start()
    telegram_app = ApplicationBuilder().token(TOKEN).build()
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CallbackQueryHandler(unlock, pattern="^unlock$"))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_message))
    telegram_app.run_polling()

if __name__ == '__main__':
    main()
