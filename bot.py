import os
import random
import datetime
import threading
from dotenv import load_dotenv
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters, ChatMemberHandler
)

# Load token from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize user data
user_captcha_answers = {}
user_language = {}

# Multilingual content with flags
menu_content = {
    "English": {
        "flag": "🇺🇸",
        "buttons": {
            "contact": "📞 Contact Admin",
            "rules": "📋 View Rules",
            "language": "🌐 Change Language",
            "back": "🔙 Back",
            "add_to_group": "➕ Add to Group",
            "send_message": "✉️ Send Message"
        },
        "rules_text": """📋 <b>Group Help Bot</b> was developed in PHP and has been online since April 13, 2016, with ongoing updates!

<b>Bot Version:</b> 10.9

<b>Bot Admins:</b> 
• Developer: Swygen Official  
• The Doctor: Server Manager  
• Manuel: Developer  
• M4R10: Support Director

⚠️ Bot staff cannot assist with group issues using this bot.

<b>Thanks</b> to all donors who support server and development costs, and to those who reported bugs or suggested features.

<b>We appreciate all groups who rely on our bot!</b>""",
        "group_welcome": """✅ <b>Welcome {name}</b>, feel free to contact - @Swygen_bd"""
    },
    "Bangla": {
        "flag": "🇧🇩",
        "buttons": {
            "contact": "📞 অ্যাডমিনের সাথে যোগাযোগ",
            "rules": "📋 রুলস দেখুন",
            "language": "🌐 ভাষা পরিবর্তন করুন",
            "back": "🔙 ফিরে যান",
            "add_to_group": "➕ গ্রুপে যুক্ত করুন",
            "send_message": "✉️ মেসেজ পাঠান"
        },
        "rules_text": """📋 <b>Group Help Bot</b> PHP-এ তৈরি এবং ১৩ এপ্রিল ২০১৬ থেকে চালু আছে নিয়মিত আপডেটসহ।

<b>বট সংস্করণ:</b> 10.9

<b>বট অ্যাডমিন:</b>  
• ডেভেলপার: Swygen Official  
• The Doctor: সার্ভার ম্যানেজার  
• Manuel: ডেভেলপার  
• M4R10: সহায়তা পরিচালক

⚠️ বট কর্মীরা এই বটের মাধ্যমে গ্রুপ সমস্যায় সহায়তা করতে পারবে না।

<b>ধন্যবাদ</b> সবাইকে যারা সার্ভার ও ডেভেলপমেন্টে সাহায্য করেছেন এবং বাগ রিপোর্ট করেছেন বা পরামর্শ দিয়েছেন।

<b>যেসব গ্রুপ আমাদের বট ব্যবহার করে, তাদের কৃতজ্ঞতা!</b>""",
        "group_welcome": """✅ <b>Welcome {name}</b>, প্রয়োজনে যোগাযোগ করুন - @Swygen_bd"""
    }
}

# Flask app setup for keep-alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Swygen Help Bot is running!"

def keep_alive():
    app.run(host='0.0.0.0', port=8080)

# Utility
def generate_captcha():
    num1 = random.randint(10, 99)
    num2 = random.randint(10, 99)
    op = random.choice(['+', '-'])
    question = f"{num1} {op} {num2}"
    answer = eval(question)
    return question, answer

def get_buttons(lang):
    buttons = menu_content[lang]["buttons"]
    return [
        [InlineKeyboardButton(buttons["contact"], url="https://t.me/Swygen_bd")],
        [InlineKeyboardButton(buttons["rules"], callback_data="rules")],
        [InlineKeyboardButton(buttons["language"], callback_data="language")],
        [InlineKeyboardButton(buttons["add_to_group"], url="https://t.me/Swygen_bot?startgroup=true")]
    ]

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    question, answer = generate_captcha()
    user_captcha_answers[user.id] = answer
    user_language[user.id] = "Bangla"
    await update.message.reply_text(
        f"🔐 <b>ভেরিফিকেশনের জন্য প্রশ্ন:</b>\n\n{question} = ?",
        parse_mode="HTML"
    )

# Handle answers
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id in user_captcha_answers:
        try:
            if int(update.message.text.strip()) == user_captcha_answers[user.id]:
                del user_captcha_answers[user.id]
                await send_welcome(update, context, new=True)
            else:
                await update.message.reply_text("❌ ভুল উত্তর! আবার চেষ্টা করুন।")
        except ValueError:
            await update.message.reply_text("⚠️ শুধু সংখ্যা দিন।")
    else:
        await update.message.reply_text("➤ অনুগ্রহ করে /start দিয়ে শুরু করুন।")

# Welcome message
async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE, new=False):
    user = update.effective_user
    lang = user_language.get(user.id, "Bangla")
    now = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=6)))
    weekday = now.strftime('%A')
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%I:%M:%S %p')
    text = f"""✅ <b>Welcome <a href='tg://user?id={user.id}'>{user.first_name}</a></b>\n\n<b>Name:</b> {user.full_name}\n<b>ID:</b> <code>{user.id}</code>\n<b>Username:</b> @{user.username or 'None'}\n<b>Date & Time:</b> {weekday}, {date} – {time}\n<b>Bot Name:</b> Swygen Help Bot\n\n{menu_content[lang]['rules_text']}"""
    markup = InlineKeyboardMarkup(get_buttons(lang))
    if new:
        await update.message.reply_html(text, reply_markup=markup)
    else:
        await update.callback_query.message.edit_text(text, parse_mode="HTML", reply_markup=markup)

# Button handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    lang = user_language.get(user.id, "Bangla")

    if query.data == "rules":
        await query.message.edit_text(menu_content[lang]['rules_text'], parse_mode="HTML")
    elif query.data == "language":
        lang_buttons = [
            [InlineKeyboardButton(f"{menu_content[l]['flag']} {l}", callback_data=f"lang_{l}")]
            for l in menu_content
        ]
        lang_buttons.append([InlineKeyboardButton(menu_content["English"]['buttons']['back'], callback_data="back")])
        await query.message.edit_text(
            text="🌐 <b>Select your language:</b>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(lang_buttons)
        )
    elif query.data.startswith("lang_"):
        selected_lang = query.data.split("_")[1]
        user_language[user.id] = selected_lang
        await send_welcome(update, context, new=False)
    elif query.data == "back":
        await send_welcome(update, context, new=False)

# Group welcome
async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = update.chat_member
    if member.new_chat_member.status == ChatMember.MEMBER:
        user = member.new_chat_member.user
        lang = user_language.get(user.id, "Bangla")
        message = menu_content[lang]['group_welcome'].format(name=user.first_name)
        button = InlineKeyboardButton(menu_content[lang]['buttons']['send_message'], url="https://t.me/Swygen_bd")
        await context.bot.send_message(chat_id=update.chat_member.chat.id, text=message, parse_mode="HTML", reply_markup=InlineKeyboardMarkup([[button]]))

# Run bot
if __name__ == "__main__":
    threading.Thread(target=keep_alive).start()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(ChatMemberHandler(welcome_new_member, ChatMemberHandler.CHAT_MEMBER))
    app.run_polling()
