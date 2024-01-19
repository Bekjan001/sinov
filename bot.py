from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import logging

# Botning maxfiy kaliti
TOKEN = "6638637683:AAHTvrP2W_fV60_m0ps60cotIGYCqTdfmuY"

# Yangi foydalanuvchilarni sanab borish uchun dictionary
user_counts = {1820810474}

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    # Agar foydalanuvchi avval ro'yxatdan o'tmagan bo'lsa, uni ro'yxatga olish
    if user_id not in user_counts:
        user_counts[user_id] = 0

    # Kanalga obuna bo'lish uchun tugma
    subscribe_button = InlineKeyboardButton("Kanalga obuna bo'lish", url="https://t.me/aliyibnvohid2023")
    subscribe_button = InlineKeyboardButton("Kanalga obuna bo'lish", url="https://t.me/aodinadoo")
    # Referal havolasini generatsiya qilish
    referral_link = f"https://t.me/your_bot_username?start={user_id}"
    referral_button = InlineKeyboardButton("Referal havolani ulashish", url=referral_link)
    # Tugmani yuborish
    update.message.reply_text("Assalomu alaykum! Botimizga xush kelibsiz!", reply_markup=InlineKeyboardMarkup([[subscribe_button], [referral_button]]))

def referral_handler(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    # Referal havolasini olish
    referral_link = f"https://t.me/your_bot_username?start={user_id}"
    update.message.reply_text(f"Sizning referal havolangiz: {referral_link}")

def check_referral_counts(context: CallbackContext) -> None:
    # Umumiy foydalanuvchi sonini kuzatib boramiz
    total_users = len(user_counts)
    logging.info(f"Jami foydalanuvchilar soni: {total_users}")

    # Agar foydalanuvchi soni belgilangan miqdordan oshgan bo'lsa, kanalga chiqish tugmasini yuboramiz
    if total_users >= 5:
        logging.info("5 foydalanuvchi to'ldi! Kanalga chiqamiz.")
        # Kanalga chiqish tugmasi
        channel_button = InlineKeyboardButton("SHu kanalga obuna bo'lishingiz mumkun", url="https://t.me/+xjp31KFuO4Q4YTA6")
        # Tugmani yuborish
        for user_id in user_counts:
            context.bot.send_message(user_id, "Tabriklaymiz! 5 ta do'stingizni taklif qilganingiz uchun rahmat! Siz kanalga obuna bo'ldingiz!", reply_markup=InlineKeyboardMarkup([[channel_button]]))

def main() -> None:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Botni yaratish
    updater = Updater(TOKEN)

    # Komandalarni qo'shish
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.regex(r'^/start \d+$'), referral_handler))  # Referal havolasi qabul qilish

    # Foydalanuvchi sonini tekshirish va kanalga chiqish tugmasini yuborish
    updater.job_queue.run_repeating(check_referral_counts, interval=60, first=0)

    # Botni ishga tushirish
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
