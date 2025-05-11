import logging
import random
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from keep_alive import keep_alive

BOT_TOKEN = "8103536905:AAGvU15mezXEXz4ezRktBofP2kf1N7K7-BU"  # আপনার Bot Token দিন
ADMIN_USERNAME = "Swygen_bd"
VERIFIED_ICON = "https://iili.io/3vOicdu.png"
RULES = "1. স্প্যাম করবেন না।\n2. অশ্লীল কথা বলবেন না।\n3. গ্রুপে সক্রিয় থাকুন।\n4. কারও প্রাইভেসি লঙ্ঘন করবেন না।"

logging.basicConfig(level=logging.INFO)

OTP_VERIFICATION = range(1)
user_otps = {}

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    otp = str(random.randint(100000, 999999))
    user_otps[user.id] = otp

    # OTP ইনবক্সে পাঠানো
    try:
        await context.bot.send_message(
            chat_id=user.id,
            text=f"আপনার OTP কোড: *{otp}*\n\nদয়া করে বট এ গিয়ে এই কোডটি লিখুন।",
            parse_mode="Markdown"
        )
    except:
        await update.message.reply_text("অনুগ্রহ করে Bot কে Start করে নিন: https://t.me/{}".format(context.bot.username))
        return ConversationHandler.END

    await update.message.reply_text("আমরা আপনার ইনবক্সে OTP পাঠিয়েছি। অনুগ্রহ করে কোডটি এখানে লিখুন:")
    return OTP_VERIFICATION

# OTP হ্যান্ডলার
async def otp_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    entered_otp = update.message.text.strip()

    if user.id not in user_otps or entered_otp != user_otps[user.id]:
        await update.message.reply_text("❌ ভুল OTP! দয়া করে সঠিক কোডটি লিখুন।")
        return OTP_VERIFICATION

    del user_otps[user.id]  # একবার ভেরিফাই হলে ডিলিট করে দিচ্ছি

    now = datetime.datetime.now()
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    badge = f"🟦 [Verified]({VERIFIED_ICON})"

    welcome_text = (
        f"**স্বাগতম {mention} {badge}**\n\n"
        f"**আপনার নাম:** {user.first_name} {user.last_name or ''}\n"
        f"**আইডি:** `{user.id}`\n"
        f"**ইউজারনেম:** @{user.username or 'N/A'}\n"
        f"**তারিখ ও সময়:** {now.strftime('%A, %d-%m-%Y – %I:%M %p')}\n"
        f"**বট নাম:** {context.bot.name}\n\n"
        f"**আমাদের সার্ভিস -**\n"
        f"• All Type App Development\n"
        f"• All Type Website Development\n"
        f"• Bot Development\n"
        f"• Support IT\n"
        f"• Automation\n"
        f"• Promote\n"
        f"• Customer Service\n\n"
        f"🌐 আমাদের ওয়েবসাইট: [swygen.netlify.app](https://swygen.netlify.app/)\n\n"
        f"📜 অনুগ্রহ করে আমাদের নিয়মাবলী পড়ুন: নিচের 'Rules' বাটনে ক্লিক করুন\n\n"
        f"✨ শুভকামনা রইলো!\n— *Swygen*"
    )

    keyboard = [
        [InlineKeyboardButton("📩 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME}")],
        [InlineKeyboardButton("📜 Rules", callback_data="rules")]
    ]

    await update.message.reply_markdown(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True
    )
    return ConversationHandler.END

# Rules Callback
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "rules":
        await query.message.reply_text(f"📜 **Rules:**\n\n{RULES}", parse_mode="Markdown")

# Cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ভেরিফিকেশন বাতিল করা হয়েছে।")
    return ConversationHandler.END

# Main
if __name__ == "__main__":
    keep_alive()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={OTP_VERIFICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, otp_handler)]},
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.COMMAND, cancel))
    app.add_handler(MessageHandler(filters.TEXT, cancel))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(CommandHandler("rules", button_handler))
    app.add_handler(MessageHandler(filters.ALL, cancel))
    app.add_handler(telegram.ext.CallbackQueryHandler(button_handler))

    print("✅ Bot is running...")
    app.run_polling()
