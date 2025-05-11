import os import logging import random import string from datetime import datetime from pytz import timezone from flask import Flask from threading import Thread from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode) from telegram.ext import (ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler)

Logging setup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

Constants

VERIFY, CAPTCHA = range(2) verified_users = {} captcha_codes = {}

Flask app for keep-alive

app_flask = Flask('')

@app_flask.route('/') def home(): return "Bot is alive!"

def run_flask(): app_flask.run(host='0.0.0.0', port=8080)

Thread(target=run_flask).start()

Handlers

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id if verified_users.get(user_id): await welcome_message(update, context) return ConversationHandler.END

code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
captcha_codes[user_id] = code
await context.bot.send_message(chat_id=user_id, text=f"🔐 Captcha Verification Code: *{code}*\n\nPlease send this code here to verify you're human.", parse_mode=ParseMode.MARKDOWN)
return CAPTCHA

async def captcha_handler(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id user_input = update.message.text.strip().upper()

if captcha_codes.get(user_id) == user_input:
    verified_users[user_id] = True
    del captcha_codes[user_id]
    await welcome_message(update, context)
    return ConversationHandler.END
else:
    await update.message.reply_text("❌ Incorrect Captcha. Please type the correct one sent to you.")
    return CAPTCHA

async def welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE): user = update.effective_user now = datetime.now(timezone('Asia/Dhaka')) time_str = now.strftime("%A, %d %B %Y – %I:%M %p")

message = f"""

✅ স্বাগতম {user.full_name} ᐧ  

আপনার নাম: {user.full_name}
আইডি: {user.id}
ইউজারনেম: @{user.username if user.username else "N/A"}
বর্তমান সময়: {time_str}
বট নাম: {context.bot.name}

আমাদের সার্ভিস - • All Type App Development • All Type Website Development • Bot Development • Support IT • Automation • Promote • Customer Service

🌐 ওয়েবসাইট: Visit Now

📌 অনুগ্রহ করে আমাদের নিয়মাবলী পড়ুন: 👇 """ keyboard = [[ InlineKeyboardButton("📋 নিয়মাবলী পড়ুন", callback_data="rules"), InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Swygen_bd") ]] reply_markup = InlineKeyboardMarkup(keyboard) await context.bot.send_message(chat_id=user.id, text=message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup, disable_web_page_preview=True)

async def rules_handler(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query await query.answer() message = """ 📜 নিয়মাবলী:

1. অশ্লীল, অপমানজনক বা অবাঞ্ছিত ভাষা ব্যবহার করা নিষিদ্ধ।


2. সবার প্রতি শ্রদ্ধাশীল আচরণ করতে হবে।


3. বারবার অপ্রয়োজনীয় মেসেজ পাঠানো যাবে না।


4. কোনরূপ প্রতারণা বা ফেক পেমেন্ট করলে স্থায়ীভাবে ব্যান করা হবে।


5. অ্যাডমিনের নির্দেশ মানতে বাধ্য থাকবেন।



⚠️ নিয়ম ভাঙলে কড়া ব্যবস্থা নেওয়া হবে। """ keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]] await query.edit_message_text(text=message, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(keyboard))

async def back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query await query.answer() await welcome_message(update, context)

def main(): TOKEN = os.getenv("BOT_TOKEN") app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        CAPTCHA: [MessageHandler(filters.TEXT & ~filters.COMMAND, captcha_handler)],
    },
    fallbacks=[]
)

app.add_handler(conv_handler)
app.add_handler(CallbackQueryHandler(rules_handler, pattern="^rules$"))
app.add_handler(CallbackQueryHandler(back_handler, pattern="^back$"))

print("Bot is running...")
app.run_polling()

if name == 'main': main()

