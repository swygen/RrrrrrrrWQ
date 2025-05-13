import os import random import datetime import threading from dotenv import load_dotenv from flask import Flask from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember from telegram.ext import ( ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters, ChatMemberHandler )

Load token from .env file

load_dotenv() BOT_TOKEN = os.getenv("BOT_TOKEN")

Initialize user data

user_captcha_answers = {} user_language = {}

Define multilingual content with flags

menu_content = { "English": { "flag": "\ud83c\uddec\ud83c\udde7", "buttons": { "contact": "\ud83d\udcde Contact Admin", "rules": "\ud83d\udccc View Rules", "language": "\ud83c\udf10 Change Language", "back": "\ud83d\udd19 Back", "add_to_group": "\u2795 Add to Group", "send_message": "\u2709\ufe0f Send Message" }, "rules_text": """\ud83d\udccc <b>Group Help Bot</b> was developed in PHP and has been online since April 13, 2016, with ongoing updates!

<b>Bot Version:</b> 10.9

<b>Bot Admins:</b>\n• Developer: Swygen Official  \n• The Doctor: Server Manager  \n• Manuel: Developer  \n• M4R10: Support Director

\u26a0\ufe0f Bot staff cannot assist with group issues using this bot.

<b>Thanks</b> to all donors who support server and development costs, and to those who reported bugs or suggested features.

<b>We appreciate all groups who rely on our bot!</b>""", "group_welcome": "\u2705 <b>Welcome {name}</b>, feel free to contact - @Swygen_bd" }, "Bangla": { "flag": "\ud83c\udded\ud83c\uddf9", "buttons": { "contact": "\ud83d\udcde \u0985\u09cd\u09af\u09be\u09a1\u09ae\u09bf\u09a8\u09c7\u09b0 \u09b8\u09be\u09a5\u09c7 \u09af\u09cb\u0997\u09be\u099c\u09cb\u0997", "rules": "\ud83d\udccc \u09b0\u09c1\u09b2\u09b8 \u09a6\u09c7\u0996\u09c1\u09a8", "language": "\ud83c\udf10 \u09ad\u09be\u09b7\u09be \u09aa\u09b0\u09bf\u09ac\u09b0\u09cd\u09a4\u09a8 \u0995\u09b0\u09c1\u09a8", "back": "\ud83d\udd19 \u09ab\u09bf\u09b0\u09c7 \u09af\u09be\u09a8", "add_to_group": "\u2795 \u0997\u09cd\u09b0\u09c1\u09aa\u09c7 \u09af\u09c1\u0995\u09cd\u09a4 \u0995\u09b0\u09c1\u09a8", "send_message": "\u2709\ufe0f \u09ae\u09c7\u09b8\u09c7\u099c \u09aa\u09be\u09a0\u09be\u09a8" }, "rules_text": """\ud83d\udccc <b>Group Help Bot</b> PHP-\u098f \u09a4\u09c8\u09b0\u09bf \u098f\u09ac\u0982 ১৩ \u098f\u09aa\u09cd\u09b0\u09bf\u09b2 ২০১৬ \u09a5\u09c7\u0995\u09c7 \u099a\u09be\u09b2\u09c1 \u0986\u099b\u09c7 \u09a8\u09bf\u09df\u09ae\u09bf\u09a4 \u0986\u09aa\u09a1\u09c7\u099f\u09b8\u09b9\u09b9।\n <b>\u09ac\u099f \u09b8\u0982\u09b8\u09cd\u0995\u09b0\u09a3:</b> 10.9

<b>\u09ac\u099f \u0985\u09cd\u09af\u09be\u09a1\u09ae\u09bf\u09a8:</b>  \n• \u09a1\u09c7\u09ad\u09c7\u09b2\u09aa\u09be\u09b0: Swygen Official  \n• The Doctor: সার্ভার ম্যানেজার  \n• Manuel: \u09a1\u09c7\u09ad\u09c7\u09b2\u09aa\u09be\u09b0  \n• M4R10: সহায়তা পরিচালক

\u26a0\ufe0f \u09ac\u099f \u0995\u09b0\u09cd\u09ae\u09c0\u09b0\u09be \u098f\u0987 \u09ac\u099f\u09c7\u09b0 \u09ae\u09be\u09a7\u09cd\u09af\u09ae\u09c7 \u0997\u09cd\u09b0\u09c1\u09aa \u09b8\u09ae\u09b8\u09cd\u09af\u09be\u09df \u09b8\u09be\u09b9\u09be\u09df\u09a4\u09be \u0995\u09b0\u09a4\u09c7 \u09aa\u09be\u09b0\u09ac\u09c7 \u09a8\u09be।

<b>\u09a7\u09a8\u09cd\u09af\u09ac\u09be\u09a6</b> সবাইকে যারা সার্ভার ও ডেভেলপমেন্টে সাহায্য করেছেন এবং বাগ রিপোর্ট করেছেন বা পরামর্শ দিয়েছেন।

<b>যেসব গ্রুপ আমাদের বট ব্যবহার করে, তাদের কৃতজ্ঞতা!</b>""", "group_welcome": "\u2705 <b>Welcome {name}</b>, প্রয়োজনে যোগাযোগ করুন - @Swygen_bd" } }

Flask keep-alive setup

app = Flask(name)

@app.route('/') def home(): return "Swygen Help Bot is running!"

def keep_alive(): app.run(host='0.0.0.0', port=8080)

Utility functions

def generate_captcha(): num1 = random.randint(10, 99) num2 = random.randint(10, 99) op = random.choice(['+', '-']) question = f"{num1} {op} {num2}" answer = eval(question) return question, answer

def get_buttons(lang): buttons = menu_content[lang]["buttons"] return [ [InlineKeyboardButton(buttons["contact"], url="https://t.me/Swygen_bd")], [InlineKeyboardButton(buttons["rules"], callback_data="rules")], [InlineKeyboardButton(buttons["language"], callback_data="language")], [InlineKeyboardButton(buttons["add_to_group"], url="https://t.me/Swygen_bot?startgroup=true")] ]

Handlers

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): user = update.effective_user question, answer = generate_captcha() user_captcha_answers[user.id] = answer user_language[user.id] = "Bangla" await update.message.reply_text( f"\ud83d\udd10 <b>ভেরিফিকেশনের জন্য প্রশ্ন:</b>\n\n{question} = ?", parse_mode="HTML" )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE): user = update.effective_user if user.id in user_captcha_answers: try: if int(update.message.text.strip()) == user_captcha_answers[user.id]: del user_captcha_answers[user.id] await send_welcome(update, context, new=True) else: await update.message.reply_text("\u274c ভুল উত্তর! আবার চেষ্টা করুন।") except ValueError: await update.message.reply_text("\u26a0\ufe0f শুধু সংখ্যা দিন।") else: await update.message.reply_text("\u2794 অনুগ্রহ করে /start দিয়ে শুরু করুন।")

async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE, new=False): user = update.effective_user lang = user_language.get(user.id, "Bangla") now = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=6))) weekday = now.strftime('%A') date = now.strftime('%Y-%m-%d') time = now.strftime('%I:%M:%S %p') text = f"""\u2705 <b>Welcome <a href='tg://user?id={user.id}'>{user.first_name}</a></b>\n\n<b>Name:</b> {user.full_name}\n<b>ID:</b> <code>{user.id}</code>\n<b>Username:</b> @{user.username or 'None'}\n<b>Date & Time:</b> {weekday}, {date} – {time}\n<b>Bot Name:</b> Swygen Help Bot\n\n{menu_content[lang]['rules_text']}""" markup = InlineKeyboardMarkup(get_buttons(lang)) if new: await update.message.reply_html(text, reply_markup=markup) else: await update.callback_query.message.edit_text(text, parse_mode="HTML", reply_markup=markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query await query.answer() user = query.from_user lang = user_language.get(user.id, "Bangla")

if query.data == "rules":
    await query.message.edit_text(menu_content[lang]['rules_text'], parse_mode="HTML")
elif query.data == "language":
    lang_buttons = [
        [InlineKeyboardButton(f"{menu_content[l]['flag']} {l}", callback_data=f"lang_{l}")]
        for l in menu_content
    ]
    lang_buttons.append([
        InlineKeyboardButton(menu_content[lang]['buttons']['back'], callback_data="back")
    ])
    await query.message.edit_text(
        text="\ud83c\udf10 <b>Select your language:</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(lang_buttons)
    )
elif query.data.startswith("lang_"):
    selected_lang = query.data.split("_")[1]
    user_language[user.id] = selected_lang
    await send_welcome(update, context, new=False)
elif query.data == "back":
    await send_welcome(update, context, new=False)

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE): member = update.chat_member if member.new_chat_member.status == ChatMember.MEMBER: user = member.new_chat_member.user lang = user_language.get(user.id, "Bangla") message = menu_content[lang]['group_welcome'].format(name=user.first_name) keyboard = InlineKeyboardButton(menu_content[lang]['buttons']['send_message'], url="https://t.me/Swygen_bd") await context.bot.send_message(chat_id=update.chat_member.chat.id, text=message, parse_mode="HTML", reply_markup=InlineKeyboardMarkup([[keyboard]]))

Start bot

if name == "main": threading.Thread(target=keep_alive).start() app = ApplicationBuilder().token(BOT_TOKEN).build() app.add_handler(CommandHandler("start", start)) app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) app.add_handler(CallbackQueryHandler(button_handler)) app.add_handler(ChatMemberHandler(welcome_new_member, ChatMemberHandler.CHAT_MEMBER)) app.run_polling()

