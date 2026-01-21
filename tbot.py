import logging
import os
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler
)

# ================= CONFIG =================
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN Render Environment’da yo‘q!")

# ================= LOGGING =================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ================= STATES =================
NAME, PHONE, SERVICE = range(3)

# ================= TRANSLATIONS =================
TRANSLATIONS = {
    "ru": {
        "welcome": "👋 Добро пожаловать в Fitness Club!\n\nВыберите нужный раздел:",
        "info": "ℹ️ Инфо",
        "booking": "📝 Заявка",
        "contact": "📞 Контакты",
        "address": "📍 Адрес",
        "language": "🌐 Язык",
        "social": "📱 Соцсети",
        "info_text": "💪 Residence Fitness Club\n\n⏰ 07:00–23:00\n🏋️‍♂️ Тренировки\n🏊‍♀️ Бассейн\n🔥 Групповые занятия",
        "contact_text": "📞 Телефон: +998997331515",
        "select_lang": "🌐 Выберите язык:",
        "lang_changed": "✅ Язык изменен",
        "enter_name": "👤 Введите имя и фамилию:",
        "share_phone": "📱 Поделитесь номером:",
        "select_service": "🏋️ Выберите услугу:",
        "pricing": "💰 Прайсинг",
        "swimming": "🏊 Плавание",
        "fitness": "🏋️ Фитнес",
        "group": "👥 Групповые",
        "other": "📋 Другое",
        "booking_sent": "✅ Заявка отправлена!",
        "cancel": "❌ Отмена",
        "cancelled": "❌ Отменено"
    },
    "uz": {
        "welcome": "👋 Fitness Club ga xush kelibsiz!\n\nBo‘limni tanlang:",
        "info": "ℹ️ Info",
        "booking": "📝 Ariza",
        "contact": "📞 Kontakt",
        "address": "📍 Manzil",
        "language": "🌐 Til",
        "social": "📱 Ijtimoiy",
        "info_text": "💪 Residence Fitness Club\n\n⏰ 07:00–23:00\n🏋️‍♂️ Mashg‘ulotlar\n🏊‍♀️ Basseyn\n🔥 Guruh treninglar",
        "contact_text": "📞 Telefon: +998997331515",
        "select_lang": "🌐 Tilni tanlang:",
        "lang_changed": "✅ Til o‘zgardi",
        "enter_name": "👤 Ism va familiya:",
        "share_phone": "📱 Telefon raqam:",
        "select_service": "🏋️ Xizmatni tanlang:",
        "pricing": "💰 Narxlar",
        "swimming": "🏊 Suzish",
        "fitness": "🏋️ Fitnes",
        "group": "👥 Guruh",
        "other": "📋 Boshqa",
        "booking_sent": "✅ Ariza yuborildi!",
        "cancel": "❌ Bekor qilish",
        "cancelled": "❌ Bekor qilindi"
    },
    "en": {
        "welcome": "👋 Welcome to Fitness Club!\n\nChoose a section:",
        "info": "ℹ️ Info",
        "booking": "📝 Booking",
        "contact": "📞 Contact",
        "address": "📍 Address",
        "language": "🌐 Language",
        "social": "📱 Social",
        "info_text": "💪 Residence Fitness Club\n\n⏰ 07:00–23:00\n🏋️ Training\n🏊 Pool\n🔥 Group classes",
        "contact_text": "📞 Phone: +998997331515",
        "select_lang": "🌐 Select language:",
        "lang_changed": "✅ Language changed",
        "enter_name": "👤 Full name:",
        "share_phone": "📱 Phone number:",
        "select_service": "🏋️ Select service:",
        "pricing": "💰 Pricing",
        "swimming": "🏊 Swimming",
        "fitness": "🏋️ Fitness",
        "group": "👥 Group",
        "other": "📋 Other",
        "booking_sent": "✅ Booking sent!",
        "cancel": "❌ Cancel",
        "cancelled": "❌ Cancelled"
    }
}

user_languages = {}

# ================= HELPERS =================
def t(user_id, key):
    return TRANSLATIONS[user_languages.get(user_id, "ru")][key]

def main_keyboard(user_id):
    return ReplyKeyboardMarkup(
        [
            [t(user_id, "info"), t(user_id, "booking")],
            [t(user_id, "contact"), t(user_id, "address")],
            [t(user_id, "language"), t(user_id, "social")]
        ],
        resize_keyboard=True
    )

# ================= HANDLERS =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_languages.setdefault(uid, "ru")
    await update.message.reply_text(t(uid, "welcome"), reply_markup=main_keyboard(uid))

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text

    if text in ["🇷🇺 Русский", "🇺🇿 O'zbekcha", "🇬🇧 English"]:
        user_languages[uid] = {"🇷🇺 Русский": "ru", "🇺🇿 O'zbekcha": "uz", "🇬🇧 English": "en"}[text]
        await update.message.reply_text(t(uid, "lang_changed"), reply_markup=main_keyboard(uid))
        return

    if text == t(uid, "info"):
        await update.message.reply_text(t(uid, "info_text"), reply_markup=main_keyboard(uid))
    elif text == t(uid, "contact"):
        await update.message.reply_text(t(uid, "contact_text"), reply_markup=main_keyboard(uid))
    elif text == t(uid, "address"):
        await update.message.reply_location(41.3697283, 69.2723819)
    elif text == t(uid, "language"):
        await update.message.reply_text(
            t(uid, "select_lang"),
            reply_markup=ReplyKeyboardMarkup(
                [["🇷🇺 Русский", "🇺🇿 O'zbekcha"], ["🇬🇧 English"]],
                resize_keyboard=True
            )
        )
    elif text == t(uid, "social"):
        await update.message.reply_text("📱 Instagram: coming soon", reply_markup=main_keyboard(uid))
    else:
        await update.message.reply_text("❗ Menyudan tanlang.", reply_markup=main_keyboard(uid))

# ============== BOOKING FLOW ==============
async def start_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    await update.message.reply_text(t(uid, "enter_name"), reply_markup=ReplyKeyboardRemove())
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    uid = update.effective_user.id
    kb = [[KeyboardButton(t(uid, "share_phone"), request_contact=True)]]
    await update.message.reply_text(t(uid, "share_phone"), reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.contact.phone_number if update.message.contact else update.message.text
    uid = update.effective_user.id
    await update.message.reply_text(
        t(uid, "select_service"),
        reply_markup=ReplyKeyboardMarkup(
            [[t(uid, "pricing"), t(uid, "swimming")],
             [t(uid, "fitness"), t(uid, "group")],
             [t(uid, "other")]],
            resize_keyboard=True
        )
    )
    return SERVICE

async def get_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    context.user_data["service"] = update.message.text

    if ADMIN_ID != 0:
        await context.bot.send_message(
            ADMIN_ID,
            f"📝 New booking\n\n"
            f"👤 {context.user_data['name']}\n"
            f"📱 {context.user_data['phone']}\n"
            f"🏋️ {context.user_data['service']}"
        )

    await update.message.reply_text(t(uid, "booking_sent"), reply_markup=main_keyboard(uid))
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    await update.message.reply_text(t(uid, "cancelled"), reply_markup=main_keyboard(uid))
    return ConversationHandler.END

# ================= MAIN =================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("📝"), start_booking)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.CONTACT | filters.TEXT, get_phone)],
            SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_service)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("✅ Bot ishga tushdi")
    app.run_polling()

if __name__ == "__main__":
    main()
