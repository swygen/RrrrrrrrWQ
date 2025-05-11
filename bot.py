import random
import datetime
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# OTP স্টোর করার জন্য ডিকশনারি
otp_data = {}

# BOT TOKEN
BOT_TOKEN = "8103536905:AAGvU15mezXEXz4ezRktBofP2kf1N7K7-BU"

# ভেরিফিকেশন ব্যাজ (ফেসবুক স্টাইল ইমেজ)
VERIFIED_BADGE = '<img src="https://iili.io/3vOicdu.png" width="20"/>'

# নিয়মাবলী
RULES_TEXT = """
<b>নিয়মাবলী:</b>

1. কাউকে অপমান করবেন না।
2. ভুয়া তথ্য প্রদান করলে ব্যান করা হবে।
3. আমাদের সেবা ব্যবহার করলে শর্ত মেনে চলতে হবে।
4. অটোমেশন বা বট স্প্যাম সম্পূর্ণ নিষিদ্ধ।
5. আপনার একাউন্ট নিরাপদ রাখুন, কারো সাথে OTP শেয়ার করবেন না।

<b>ধন্যবাদ!</b>
"""

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # র‍্যান্ডম OTP তৈরি
    otp = str(random.randint(1000, 9999))
    otp_data[user.id] = otp

    try:
        # ইনবক্সে OTP পাঠানো হচ্ছে
        await context.bot.send_message(
            chat_id=user.id,
            text=f"🔐 <b>আপনার OTP:</b> <code>{otp}</code>\n\nঅনুগ্রহ করে এই OTP টি বটের ইনবক্সে লিখুন।",
            parse_mode=ParseMode.HTML
        )
        if update.message:
            await update.message.reply_text("✅ আমরা আপনার ইনবক্সে OTP পাঠিয়েছি। অনুগ্রহ করে সেখানে গিয়ে যাচাই করুন।")
    except:
        if update.message:
            await update.message.reply_text(
                "❌ অনুগ্রহ করে প্রথমে বটকে ইনবক্সে /start করে ইনবক্স চালু করুন। তারপর আবার চেষ্টা করুন।"
            )

# ইউজার OTP পাঠালে যাচাই করা হবে
async def handle_otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_otp = update.message.text.strip()

    if user.id in otp_data and user_otp == otp_data[user.id]:
        del otp_data[user.id]  # OTP মুছে ফেলা

        now = datetime.datetime.now()
        formatted_date = now.strftime("%A, %d %B %Y – %I:%M %p")

        # ইনলাইন বাটন
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Swygen_bd")],
            [InlineKeyboardButton("📜 Rules", callback_data="show_rules")]
        ])

        # প্রিমিয়াম স্বাগতম মেসেজ
        welcome_msg = f"""
<b>স্বাগতম {user.mention_html()} {VERIFIED_BADGE} আপনার আগমনে আমরা আনন্দিত!</b>

<b>নাম:</b> {user.first_name} {user.last_name or ""}  
<b>আইডি:</b> <code>{user.id}</code>  
<b>ইউজারনেম:</b> @{user.username or 'N/A'}  
<b>বর্তমান তারিখ ও সময়:</b> {formatted_date}  
<b>বট নাম:</b> {context.bot.name}

<b>আমাদের সার্ভিস:</b>
• All Type App Development  
• All Type Website Development  
• Bot Development  
• Support IT  
• Automation  
• Promote  
• Customer Service  

🌐 <b>ওয়েবসাইট:</b> https://swygen.netlify.app/

<b>অনুগ্রহ করে আমাদের নিয়মাবলী পড়ুন:</b> Rules বাটনে ক্লিক করুন

<b>শুভকামনা রইলো!</b>
— Swygen
"""
        await update.message.reply_text(welcome_msg, parse_mode=ParseMode.HTML, reply_markup=buttons)
    else:
        await update.message.reply_text("❌ ভুল OTP! অনুগ্রহ করে সঠিক OTP দিন।")

# রুলস বাটন প্রেস হলে
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "show_rules":
        await query.edit_message_text(RULES_TEXT, parse_mode=ParseMode.HTML)

# অ্যাপ রান
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_otp))
    app.add_handler(MessageHandler(filters.COMMAND, lambda u, c: u.message.reply_text("❓ অজানা কমান্ড। /start ব্যবহার করুন")))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, start))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, lambda u, c: None))
    app.add_handler(MessageHandler(filters.StatusUpdate, lambda u, c: None))
    app.add_handler(MessageHandler(filters.ALL, lambda u, c: None))
    app.add_handler(MessageHandler(filters.COMMAND, lambda u, c: None))
    app.add_handler(MessageHandler(filters.TEXT, handle_otp))
    app.add_handler(MessageHandler(filters.Regex(".*"), handle_otp))
    app.add_handler(MessageHandler(filters.UpdateType.CALLBACK_QUERY, callback_handler))

    print("✅ Bot is running...")
    app.run_polling()
