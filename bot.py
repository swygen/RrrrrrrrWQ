import os
import random
import datetime
from dotenv import load_dotenv
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)
from flask import Flask
import threading

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

user_captcha_answers = {}

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def keep_alive():
    app.run(host='0.0.0.0', port=8080)

# Captcha generator
def generate_captcha():
    num1 = random.randint(10, 99)
    num2 = random.randint(10, 99)
    op = random.choice(['+', '-'])
    question = f"{num1} {op} {num2}"
    answer = eval(question)
    return question, answer

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    question, answer = generate_captcha()
    user_captcha_answers[user.id] = answer

    await update.message.reply_text(
        f"Hello {user.first_name}, please solve this captcha to verify:\n\n{question} = ?"
    )

# Captcha answer handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id in user_captcha_answers:
        try:
            if int(update.message.text) == user_captcha_answers[user.id]:
                del user_captcha_answers[user.id]
                await send_welcome(update, context)
            else:
                await update.message.reply_text("❌ Incorrect answer! Please try again.")
        except ValueError:
            await update.message.reply_text("⚠️ Please send only numbers.")
    else:
        await update.message.reply_text("Use /start to begin.")

# Verified welcome message
async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    now = datetime.datetime.now()
    weekday = now.strftime('%A')
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%I:%M:%S %p')

    welcome_text = (
        f"✅ <b>স্বাগতম <a href='tg://user?id={user.id}'>{user.first_name}</a></b>\n\n"
        f"<b>আপনার নাম:</b> {user.first_name} {user.last_name or ''}\n"
        f"<b>আইডি:</b> <code>{user.id}</code>\n"
        f"<b>ইউজারনেম:</b> @{user.username or 'None'}\n"
        f"<b>তারিখ ও সময়:</b> {weekday}, {date} – {time}\n"
        f"<b>বট নাম:</b> {context.bot.name}\n\n"
        f"<b>আমাদের সার্ভিস:</b>\n"
        f"- All Type App Development\n"
        f"- Website Development\n"
        f"- Bot Development\n"
        f"- Support IT\n"
        f"- Automation & Promote\n\n"
        f"🌐 ওয়েবসাইট: https://swygen.netlify.app/\n"
        f"📋 নিয়মাবলী জানতে নিচের বাটনে ক্লিক করুন।"
    )

    keyboard = [
        [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Swygen_bd")],
        [InlineKeyboardButton("📋 রুলস পড়ুন", callback_data="rules")]
    ]
    await update.message.reply_html(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard))

# Rules handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "rules":
        rules = (
            "📋 <b>নিয়মাবলী:</b>\n"
            "1. অশ্লীলতা বা গালিগালাজ নিষিদ্ধ\n"
            "2. বট স্প্যাম করা যাবে না\n"
            "3. সঠিক তথ্য দিন\n"
            "4. সন্দেহজনক কার্যকলাপ করলে ব্যান করা হবে\n"
            "5. কাস্টম সার্ভিসের জন্য এডমিনের সাথে যোগাযোগ করুন\n\n"
            "✅ নিয়ম মেনে ব্যবহার করুন এবং মজা নিন!"
        )
        # Back button functionality to go back to main menu
        keyboard = [
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]
        await query.message.reply_html(rules, reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "back":
        await query.message.reply_text("🔙 You are back to the main menu.", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Swygen_bd")],
            [InlineKeyboardButton("📋 রুলস পড়ুন", callback_data="rules")]
        ]))

# Main bot runner
if __name__ == "__main__":
    threading.Thread(target=keep_alive).start()

    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()

    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_bot.add_handler(CallbackQueryHandler(button_handler))

    app_bot.run_polling()
