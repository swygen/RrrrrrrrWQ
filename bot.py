import os import random import datetime import threading from dotenv import load_dotenv from telegram import ( Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember ) from telegram.ext import ( ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters, ChatMemberHandler ) from flask import Flask

load_dotenv() BOT_TOKEN = os.getenv("BOT_TOKEN")

user_captcha_answers = {} user_language = {}

menu_content = {
    "English": {
        "buttons": {
            "contact": "📞 Contact Admin",
            "rules": "📋 View Rules",
            "language": "🌐 Language",
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
        "group_welcome": """✅ <b>Welcome Game</b>, feel free to contact - @mahtabnihar

<b>Our Services:</b> 
• Tournament App (Popular🔥)  
• Android App  
• Website  
• Digital Marketing etc.

<b>Username:</b> {username}  
<b>Joining:</b> {join_time}"""
    },

    "Bangla": {
        "buttons": {
            "contact": "📞 অ্যাডমিনের সাথে যোগাযোগ করুন",
            "rules": "📋 রুলস পড়ুন",
            "language": "🌐 ভাষা পরিবর্তন করুন",
            "back": "🔙 ফিরে যান",
            "add_to_group": "➕ গ্রুপে যুক্ত করুন",
            "send_message": "✉️ মেসেজ পাঠান"
        },
        "rules_text": """📋 <b>গ্রুপ হেল্প</b> হল একটি বট যা PHP-এ বিকশিত হয়েছে, এটি 13 এপ্রিল 2016 থেকে অনলাইনে রয়েছে এবং এটি ক্রমাগত আপডেট করা হয়!

<b>বট সংস্করণ:</b> 10.9

<b>বট অ্যাডমিন:</b>  
• ডেভেলপার: Swygen Official  
• The Doctor: সার্ভার ম্যানেজার  
• Manuel: ডেভেলপার  
• M4R10: সমর্থন পরিচালক

⚠️ বট কর্মীরা এই বট ব্যবহার করে গোষ্ঠীর সাথে জড়িত সমস্যায় সহায়তা করতে পারবে না।

<b>ধন্যবাদ</b> আমাদের সকল দাতাকে যারা সার্ভার ও ডেভেলপমেন্ট খরচে সহায়তা করেছেন এবং যারা বাগ রিপোর্ট করেছেন বা নতুন ফিচারের প্রস্তাব দিয়েছেন।

<b>যেসব গ্রুপ এই বটের উপর নির্ভর করে তাদের সবাইকে ধন্যবাদ!</b>""",
        "group_welcome": """✅ <b>Welcome Game</b>, যেকোনো প্রয়োজনে যোগাযোগ করুন - @mahtabnihar

<b>আমাদের সেবা সমূহ:</b> 
• Tournament App (Popular🔥)  
• Android App  
• Website  
• Digital Marketing ইত্যাদি

<b>Username:</b> {username}  
<b>Joining:</b> {join_time}"""
    },

    "China": {
        "buttons": {
            "contact": "📞 联系管理员",
            "rules": "📋 查看规则",
            "language": "🌐 更改语言",
            "back": "🔙 返回",
            "add_to_group": "➕ 添加到群组",
            "send_message": "✉️ 发送消息"
        },
        "rules_text": """📋 <b>Group Help Bot</b> 是一个使用 PHP 开发的机器人，自 2016 年 4 月 13 日上线以来持续更新！

<b>机器人版本:</b> 10.9

<b>管理员:</b>  
• 开发者: Swygen Official  
• The Doctor: 服务器管理员  
• Manuel: 开发人员  
• M4R10: 支持主管

⚠️ 工作人员无法通过此机器人处理群组问题。

<b>感谢所有支持者和建议者！</b>""",
        "group_welcome": """✅ <b>欢迎 Game</b>，如有需要请联系 - @mahtabnihar

<b>我们的服务:</b>  
• 比赛应用程序（热门）  
• 安卓应用  
• 网站  
• 数字营销 等等

<b>用户名:</b> {username}  
<b>加入时间:</b> {join_time}"""
    },

    "Hindi": {
        "buttons": {
            "contact": "📞 एडमिन से संपर्क करें",
            "rules": "📋 नियम देखें",
            "language": "🌐 भाषा बदलें",
            "back": "🔙 वापस जाएं",
            "add_to_group": "➕ ग्रुप में जोड़ें",
            "send_message": "✉️ संदेश भेजें"
        },
        "rules_text": """📋 <b>Group Help Bot</b> एक PHP में विकसित किया गया बॉट है, जो 13 अप्रैल 2016 से ऑनलाइन है और लगातार अपडेट होता रहता है!

<b>बॉट संस्करण:</b> 10.9

<b>बॉट एडमिन:</b>  
• डेवलपर: Swygen Official  
• The Doctor: सर्वर मैनेजर  
• Manuel: डेवलपर  
• M4R10: समर्थन निदेशक

⚠️ बॉट स्टाफ इस बॉट से ग्रुप समस्याओं में सहायता नहीं कर सकता।

<b>धन्यवाद</b> सभी दाताओं को और जिन्होंने बग रिपोर्ट या सुझाव दिए।""",
        "group_welcome": """✅ <b>Welcome Game</b>, किसी भी ज़रूरत के लिए संपर्क करें - @mahtabnihar

<b>हमारी सेवाएं:</b>  
• टूर्नामेंट ऐप (लोकप्रिय)  
• एंड्रॉइड ऐप  
• वेबसाइट  
• डिजिटल मार्केटिंग आदि

<b>यूज़रनेम:</b> {username}  
<b>जॉइनिंग:</b> {join_time}"""
    },

    "Arabic": {
        "buttons": {
            "contact": "📞 اتصل بالمسؤول",
            "rules": "📋 عرض القواعد",
            "language": "🌐 تغيير اللغة",
            "back": "🔙 رجوع",
            "add_to_group": "➕ أضف إلى المجموعة",
            "send_message": "✉️ أرسل رسالة"
        },
        "rules_text": """📋 <b>بوت Group Help</b> تم تطويره بـ PHP وهو متصل منذ 13 أبريل 2016 ويستمر تحديثه باستمرار!

<b>إصدار البوت:</b> 10.9

<b>إدارة البوت:</b>  
• المطور: Swygen Official  
• The Doctor: مدير الخادم  
• Manuel: مطور  
• M4R10: مدير الدعم

⚠️ لا يستطيع فريق البوت المساعدة في مشاكل المجموعة من خلال هذا البوت.

<b>شكرًا لجميع المتبرعين والمستخدمين!</b>""",
        "group_welcome": """✅ <b>مرحبًا Game</b>، تواصل معنا عند الحاجة - @mahtabnihar

<b>خدماتنا:</b>  
• تطبيق البطولة  
• تطبيق أندرويد  
• موقع إلكتروني  
• التسويق الرقمي وغير ذلك

<b>اسم المستخدم:</b> {username}  
<b>الانضمام:</b> {join_time}"""
    }
}

app = Flask(name)

@app.route('/') def home(): return "Swygen Help Bot is running!"

def keep_alive(): app.run(host='0.0.0.0', port=8080)

def generate_captcha(): num1 = random.randint(10, 99) num2 = random.randint(10, 99) op = random.choice(['+', '-']) question = f"{num1} {op} {num2}" answer = eval(question) return question, answer

def get_buttons(lang): buttons = menu_content[lang]["buttons"] return [ [InlineKeyboardButton(buttons["contact"], url="https://t.me/Swygen_bd")], [InlineKeyboardButton(buttons["rules"], callback_data="rules")], [InlineKeyboardButton(buttons["language"], callback_data="language")], [InlineKeyboardButton(buttons["add_to_group"], url=f"https://t.me/SwygenHelpBot?startgroup=true")] ]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): user = update.effective_user question, answer = generate_captcha() user_captcha_answers[user.id] = answer user_language[user.id] = "Bangla" await update.message.reply_text( f"🔐 <b>ভেরিফিকেশনের জন্য প্রশ্নটিটি উত্তর দিন:</b>\n\n{question} = ?", parse_mode="HTML" )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE): user = update.effective_user if user.id in user_captcha_answers: try: if int(update.message.text.strip()) == user_captcha_answers[user.id]: del user_captcha_answers[user.id] await send_welcome(update, context, new=True) else: await update.message.reply_text("❌ ভুল উত্তর! আবার চেষ্টা করুন।") except ValueError: await update.message.reply_text("⚠️ শুধু সংখ্যা দিন।") else: await update.message.reply_text("➤ অনুগ্রহ করে /start দিয়ে শুরু করুন।")

async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE, new=False): user = update.effective_user lang = user_language.get(user.id, "Bangla") now = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=6))) weekday = now.strftime('%A') date = now.strftime('%Y-%m-%d') time = now.strftime('%I:%M:%S %p')

text = f"""✅ <b>Welcome <a href='tg://user?id={user.id}'>{user.first_name}</a></b>

<b>Name:</b> {user.first_name} {user.last_name or ''} <b>ID:</b> <code>{user.id}</code> <b>Username:</b> @{user.username or 'None'} <b>Date & Time:</b> {weekday}, {date} – {time} <b>Bot Name:</b> Swygen Help Bot

{menu_content[lang]['rules_text']}""" markup = InlineKeyboardMarkup(get_buttons(lang))

if new:
    await update.message.reply_html(text, reply_markup=markup)
else:
    await update.callback_query.message.edit_text(text, parse_mode="HTML", reply_markup=markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query await query.answer() user = query.from_user lang = user_language.get(user.id, "Bangla")

if query.data == "rules":
    await query.message.edit_text(
        menu_content[lang]['rules_text'], parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(InlineKeyboardButton(menu_content[lang]['buttons']['back'], callback_data="back"))
    )
elif query.data == "language":
    langs = list(menu_content.keys())
    lang_buttons = [[InlineKeyboardButton(l, callback_data=f"lang_{l}")] for l in langs]
    lang_buttons.append([InlineKeyboardButton(menu_content[lang]['buttons']['back'], callback_data="back")])
    await query.message.edit_text("🌐 <b>Select your language:</b>", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(lang_buttons))
elif query.data.startswith("lang_"):
    selected_lang = query.data.split("_")[1]
    user_language[user.id] = selected_lang
    await send_welcome(update, context, new=False)
elif query.data == "back":
    await send_welcome(update, context, new=False)

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE): member = update.chat_member if member.new_chat_member.status == ChatMember.MEMBER: user = member.new_chat_member.user lang = user_language.get(user.id, "Bangla") now = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=6))) time_str = now.strftime("%d/%m/%Y %H:%M:%S") message = menu_content[lang]['group_welcome'].format(username=f"@{user.username or 'None'}", join_time=time_str) keyboard = InlineKeyboardButton(menu_content[lang]['buttons']['send_message'], url="https://t.me/Swygen_bd") await context.bot.send_message(chat_id=update.chat_member.chat.id, text=message, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

if name == "main": threading.Thread(target=keep_alive).start() app = ApplicationBuilder().token(BOT_TOKEN).build() app.add_handler(CommandHandler("start", start)) app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) app.add_handler(CallbackQueryHandler(button_handler)) app.add_handler(ChatMemberHandler(welcome_new_member, ChatMemberHandler.CHAT_MEMBER)) app.run_polling()

