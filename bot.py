import os
import random
import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)
from flask import Flask
import threading

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

user_captcha_answers = {}
user_language = {}

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

# Multilingual welcome messages
def get_welcome_text(user, lang, bot_name):
    now = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=6)))
    weekday = now.strftime('%A')
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%I:%M:%S %p')

    templates = {
        "English": f"""✅ <b>Welcome <a href='tg://user?id={user.id}'>{user.first_name}</a></b>

<b>Name:</b> {user.first_name} {user.last_name or ''}
<b>ID:</b> <code>{user.id}</code>
<b>Username:</b> @{user.username or 'None'}
<b>Date & Time:</b> {weekday}, {date} – {time}
<b>Bot Name:</b> {bot_name}

<b>Our Services:</b>
- All Type App Development
- Website Development
- Bot Development
- Support IT
- Automation & Promote

🌐 Website: https://swygen.netlify.app/
📋 Click the button below to read our rules.""",

        "Bangla": f"""✅ <b>স্বাগতম <a href='tg://user?id={user.id}'>{user.first_name}</a></b>

<b>আপনার নাম:</b> {user.first_name} {user.last_name or ''}
<b>আইডি:</b> <code>{user.id}</code>
<b>ইউজারনেম:</b> @{user.username or 'None'}
<b>তারিখ ও সময়:</b> {weekday}, {date} – {time}
<b>বট নাম:</b> {bot_name}

<b>আমাদের সার্ভিস:</b>
- অ্যাপ ডেভেলপমেন্ট
- ওয়েবসাইট ডেভেলপমেন্ট
- বট ডেভেলপমেন্ট
- আইটি সাপোর্ট
- অটোমেশন ও প্রোমোট

🌐 ওয়েবসাইট: https://swygen.netlify.app/
📋 নিয়মাবলী জানতে নিচের বাটনে ক্লিক করুন।""",

        "China": f"""✅ <b>欢迎 <a href='tg://user?id={user.id}'>{user.first_name}</a></b>

名称: {user.first_name} {user.last_name or ''}
ID: <code>{user.id}</code>
用户名: @{user.username or 'None'}
日期和时间: {weekday}, {date} – {time}
机器人名称: {bot_name}

服务：
- 应用开发
- 网站开发
- 机器人开发
- 技术支持
- 自动化与推广

🌐 网站: https://swygen.netlify.app/
📋 点击按钮查看规则。""",

        "Hindi": f"""✅ <b>स्वागत है <a href='tg://user?id={user.id}'>{user.first_name}</a></b>

<b>नाम:</b> {user.first_name} {user.last_name or ''}
<b>ID:</b> <code>{user.id}</code>
<b>यूज़रनेम:</b> @{user.username or 'None'}
<b>तारीख और समय:</b> {weekday}, {date} – {time}
<b>बॉट का नाम:</b> {bot_name}

<b>हमारी सेवाएं:</b>
- ऐप डेवलपमेंट
- वेबसाइट डेवलपमेंट
- बॉट डेवलपमेंट
- आईटी सपोर्ट
- ऑटोमेशन और प्रमोशन

🌐 वेबसाइट: https://swygen.netlify.app/
📋 नियम देखने के लिए नीचे बटन पर क्लिक करें।""",

        "Arabic": f"""✅ <b>مرحبًا <a href='tg://user?id={user.id}'>{user.first_name}</a></b>

<b>الاسم:</b> {user.first_name} {user.last_name or ''}
<b>المعرف:</b> <code>{user.id}</code>
<b>اسم المستخدم:</b> @{user.username or 'None'}
<b>التاريخ والوقت:</b> {weekday}, {date} – {time}
<b>اسم البوت:</b> {bot_name}

<b>خدماتنا:</b>
- تطوير التطبيقات
- تطوير المواقع
- تطوير البوت
- الدعم الفني
- الأتمتة والترويج

🌐 الموقع الإلكتروني: https://swygen.netlify.app/
📋 اضغط الزر أدناه لقراءة القواعد."""
    }
    return templates.get(lang, templates["English"])

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    question, answer = generate_captcha()
    user_captcha_answers[user.id] = answer
    user_language[user.id] = "Bangla"  # Default language

    await update.message.reply_text(
        f"🔐 <b>ভেরিফিকেশনের জন্য নিচের প্রশ্নটির উত্তর দিন:</b>\n\n{question} = ?",
        parse_mode="HTML"
    )

# Captcha answer handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id in user_captcha_answers:
        try:
            if int(update.message.text.strip()) == user_captcha_answers[user.id]:
                del user_captcha_answers[user.id]
                await send_welcome(update, context)
            else:
                await update.message.reply_text("❌ ভুল উত্তর! আবার চেষ্টা করুন।")
        except ValueError:
            await update.message.reply_text("⚠️ শুধু সংখ্যা দিন।")
    else:
        await update.message.reply_text("➤ অনুগ্রহ করে /start দিয়ে শুরু করুন।")

# Welcome message
async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = user_language.get(user.id, "Bangla")
    text = get_welcome_text(user, lang, context.bot.name)

    keyboard = [
        [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Swygen_bd")],
        [InlineKeyboardButton("📋 রুলস পড়ুন", callback_data="rules")],
        [InlineKeyboardButton("🌐 Language", callback_data="language")]
    ]
    await update.message.reply_html(text, reply_markup=InlineKeyboardMarkup(keyboard))

# Callback handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    if query.data == "rules":
        await query.message.edit_text(
            "📋 <b>নিয়মাবলী:</b>\n"
            "1. গালিগালাজ নিষিদ্ধ\n"
            "2. স্প্যাম নিষিদ্ধ\n"
            "3. ভুল তথ্য প্রদান থেকে বিরত থাকুন\n"
            "4. নিয়ম ভাঙলে ব্যান করা হতে পারে\n\n"
            "✅ নিয়ম মেনে চলুন।",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back")]])
        )
    elif query.data == "language":
        langs = ["English", "Bangla", "China", "Hindi", "Arabic"]
        lang_buttons = [[InlineKeyboardButton(lang, callback_data=f"lang_{lang}")] for lang in langs]
        lang_buttons.append([InlineKeyboardButton("🔙 Back", callback_data="back")])
        await query.message.edit_text("🌐 <b>Select your language:</b>", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(lang_buttons))
    elif query.data.startswith("lang_"):
        lang = query.data.split("_")[1]
        user_language[user.id] = lang
        await query.message.delete()
        await send_welcome(update, context)
    elif query.data == "back":
        await query.message.delete()
        await send_welcome(update, context)

# Main bot setup
if __name__ == "__main__":
    threading.Thread(target=keep_alive).start()

    bot = ApplicationBuilder().token(BOT_TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    bot.add_handler(CallbackQueryHandler(button_handler))
    bot.run_polling()
