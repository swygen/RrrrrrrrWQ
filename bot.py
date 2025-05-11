Telegram OTP Verification Bot with Welcome Message and Inline Buttons

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto from telegram.ext import ( ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler ) import random import string import datetime import asyncio import os from flask import Flask from threading import Thread

--- Flask keep-alive ---

app_flask = Flask('')

@app_flask.route('/') def home(): return "Bot is running!"

def run(): app_flask.run(host='0.0.0.0', port=8080)

def keep_alive(): t = Thread(target=run) t.start()

--- Bot States ---

ASKING_OTP, VERIFYING = range(2)

--- OTP Store ---

otp_data = {}

--- Command: /start ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: user = update.effective_user otp = ''.join(random.choices(string.digits, k=6)) otp_data[user.id] = otp

try:
    await context.bot.send_message(chat_id=user.id, text=f"Your OTP is: {otp}")
except:
    await update.message.reply_text("Please start a private chat with me and press /start again: https://t.me/YourBotUsername")
    return ConversationHandler.END

await update.message.reply_text("An OTP has been sent to your inbox. Please enter it here:")
return ASKING_OTP

--- OTP Verification ---

async def verify_otp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: user = update.effective_user user_input = update.message.text.strip()

if user.id in otp_data and otp_data[user.id] == user_input:
    del otp_data[user.id]

    now = datetime.datetime.now()
    weekday = now.strftime('%A')
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%I:%M:%S %p')

    verified_icon_url = "https://iili.io/3vOicdu.png"
    keyboard = [
        [InlineKeyboardButton("Contact Admin", url="https://t.me/Swygen_bd")],
        [InlineKeyboardButton("রুলস পড়ুন", callback_data="rules")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = f"\n✅ **স্বাগতম [{user.first_name}](tg://user?id={user.id})** <a href='{verified_icon_url}'> </a>\n\n"
    welcome_text += f"**আপনার নাম:** {user.first_name} {user.last_name or ''}\n"
    welcome_text += f"**আপনার আইডি:** `{user.id}`\n"
    welcome_text += f"**ইউজারনেম:** @{user.username or 'None'}\n"
    welcome_text += f"**বর্তমান তারিখ ও সময়:** {weekday}, {date} – {time}\n"
    welcome_text += f"**বট নাম:** {context.bot.name}\n\n"

    welcome_text += "**আমাদের সার্ভিস -**\n"
    welcome_text += "- All Type App Development\n"
    welcome_text += "- All Type Website Development\n"
    welcome_text += "- Bot Development\n"
    welcome_text += "- Support IT\n"
    welcome_text += "- Automation\n"
    welcome_text += "- Promote\n"
    welcome_text += "- Customer Service\n\n"
    welcome_text += "🌐 ওয়েবসাইট: https://swygen.netlify.app/\n\n"
    welcome_text += "**অনুগ্রহ করে আমাদের নিয়মাবলী পড়ুন নিচের বাটনে ক্লিক করে।**"

    await update.message.reply_html(welcome_text, reply_markup=reply_markup)
    return ConversationHandler.END
else:
    await update.message.reply_text("❌ ভুল OTP। অনুগ্রহ করে সঠিক OTP দিন।")
    return ASKING_OTP

--- Rules Handler ---

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query await query.answer() if query.data == "rules": await query.message.reply_text(""" নিয়মাবলী:

1. কোন প্রকার স্প্যাম করবেন না।


2. সম্মানজনক ভাষা ব্যবহার করুন।


3. বারবার OTP রিকোয়েস্ট করা যাবে না।


4. সার্ভিস ব্যবহার করার পূর্বে সম্পূর্ণ তথ্য ভালোভাবে পড়ে নিন।


5. আমাদের টিমের সাথে ভদ্রভাবে কথা বলুন। """, parse_mode='Markdown')



--- Main Function ---

async def main(): TOKEN = os.environ.get("BOT_TOKEN")  # Bot token should be set in env app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        ASKING_OTP: [MessageHandler(filters.TEXT & ~filters.COMMAND, verify_otp)],
    },
    fallbacks=[]
)

app.add_handler(conv_handler)
app.add_handler(CallbackQueryHandler(button_handler))

print("Bot is running...")
keep_alive()
await app.run_polling()

if name == 'main': import asyncio asyncio.run(main())

