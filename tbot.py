import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler


try:
    from config import BOT_TOKEN, ADMIN_ID
except ImportError:
    # Agar config.py bo'lmasa, environment variables dan olish
    import os
    BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
    ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


NAME, PHONE, SERVICE = range(3)


TRANSLATIONS = {
    'ru': {
        'welcome': '👋 Добро пожаловать в Fitness Club!\n\nВыберите нужный раздел:',
        'info': 'ℹ️ Инфо',
        'booking': '📝 Заявка',
        'contact': '📞 Контакты',
        'address': '📍 Адрес',
        'language': '🌐 Язык',
        'social': '📱 Соцсети',
        'info_text': '''💪 Добро пожаловать в Residence Fitness Club!

Residence Fitness Club — это новый, современный и комфортный фитнес-клуб для тех, кто выбирает здоровье, силу и уверенность.

⏰ Работаем 07:00-23:00
🏋️‍♂️ Фитнес-тренировки
🏊‍♀️ Бассейн и занятия по плаванию
🔥 Групповые и персональные тренировки
🌿 Чистая атмосфера и профессиональные тренеры

Каждая тренировка — шаг к лучшей версии себя.
Тренируйтесь с удовольствием и достигайте реальных результатов!

✨ Здоровый образ жизни начинается в Residence Fitness Club.''',
        'contact_text': '📞 Контакты:\n\n✨ Residence Fitness Club\n📱 Телефон: +998997331515',
        'select_lang': '🌐 Выберите язык / Tilni tanlang / Select language:',
        'lang_changed': '✅ Язык изменен',
        'enter_name': '👤 Введите ваше имя и фамилию:',
        'share_phone': '📱 Поделитесь вашим номером телефона:',
        'select_service': '🏋️ Выберите услугу:',
        'pricing': '💰 Прайсинг',
        'swimming': '🏊 Плавание',
        'fitness': '🏋️ Фитнес',
        'group': '👥 Групповые занятия',
        'other': '📋 Другое',
        'booking_sent': '✅ Ваша заявка отправлена!\n\nМы свяжемся с вами в ближайшее время.',
        'back': '🔙 Назад',
        'cancel': '❌ Отмена',
        'cancelled': '❌ Отменено'
    },
    'uz': {
        'welcome': '👋 Fitness Club ga xush kelibsiz!\n\nKerakli bo\'limni tanlang:',
        'info': 'ℹ️ Info',
        'booking': '📝 Ariza',
        'contact': '📞 Kontaktlar',
        'address': '📍 Manzil',
        'language': '🌐 Til',
        'social': '📱 Ijtimoiy tarmoqlar',
        'info_text': '''💪 Residence Fitness Club ga xush kelibsiz!

Residence Fitness Club — bu yangi ochilgan, zamonaviy va qulay fitness makoni. Biz sog'lom turmush tarzi, kuchli tana va yuqori energiyani tanlaganlar uchun ishlaymiz.

⏰ 07:00-23:00 Ochiq
🏋️‍♂️ Fitness mashg'ulotlari
🏊‍♀️ Pool va suzish mashg'ulotlari
🔥 Guruh va individual treninglar
🌿 Toza muhit va professional trenerlar

Har bir mashg'ulot — bu o'zingizga qo'yilgan investitsiya.
Natijani his qiling, formangizni o'zgartiring va o'zingizdan faxrlaning!

✨ Sog'lom hayot Residence Fitness Club'dan boshlanadi.''',
        'contact_text': '📞 Kontaktlar:\n\n✨ Residence Fitness Club\n📱 Telefon: +998997331515',
        'select_lang': '🌐 Выберите язык / Tilni tanlang / Select language:',
        'lang_changed': '✅ Til o\'zgartirildi',
        'enter_name': '👤 Ism va familiyangizni kiriting:',
        'share_phone': '📱 Telefon raqamingizni ulashing:',
        'select_service': '🏋️ Xizmatni tanlang:',
        'pricing': '💰 Narxlar',
        'swimming': '🏊 Suzish',
        'fitness': '🏋️ Fitnes',
        'group': '👥 Guruh mashg\'ulotlari',
        'other': '📋 Boshqa',
        'booking_sent': '✅ Arizangiz yuborildi!\n\nTez orada siz bilan bog\'lanamiz.',
        'back': '🔙 Ortga',
        'cancel': '❌ Bekor qilish',
        'cancelled': '❌ Bekor qilindi'
    },
    'en': {
        'welcome': '👋 Welcome to Fitness Club!\n\nChoose a section:',
        'info': 'ℹ️ Info',
        'booking': '📝 Booking',
        'contact': '📞 Contact',
        'address': '📍 Address',
        'language': '🌐 Language',
        'social': '📱 Social Media',
        'info_text': '''💪 Welcome to Residence Fitness Club!

Residence Fitness Club is a newly opened, modern and comfortable fitness destination for those who value health, strength, and balance.

⏰ Open 07:00-23:00
🏋️‍♂️ Fitness training
🏊‍♀️ Swimming pool & aquatic workouts
🔥 Group classes & personal training
🌿 Clean environment & professional coaches

Every workout is an investment in yourself.
Feel the energy, see the results, and become your best version!''',
        'contact_text': '📞 Contact:\n\n✨ Residence Fitness Club\n📱 Phone: +998997331515',
        'select_lang': '🌐 Выберите язык / Tilni tanlang / Select language:',
        'lang_changed': '✅ Language changed',
        'enter_name': '👤 Enter your full name:',
        'share_phone': '📱 Share your phone number:',
        'select_service': '🏋️ Select service:',
        'pricing': '💰 Pricing',
        'swimming': '🏊 Swimming',
        'fitness': '🏋️ Fitness',
        'group': '👥 Group Sessions',
        'other': '📋 Other',
        'booking_sent': '✅ Your booking has been sent!\n\nWe will contact you soon.',
        'back': '🔙 Back',
        'cancel': '❌ Cancel',
        'cancelled': '❌ Cancelled'
    }
}


user_languages = {}

def get_text(user_id, key):
    lang = user_languages.get(user_id, 'ru')
    return TRANSLATIONS[lang][key]

def get_main_keyboard(user_id):
    lang = user_languages.get(user_id, 'ru')
    keyboard = [
        [get_text(user_id, 'info'), get_text(user_id, 'booking')],
        [get_text(user_id, 'contact'), get_text(user_id, 'address')],
        [get_text(user_id, 'language'), get_text(user_id, 'social')]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_languages:
        user_languages[user_id] = 'ru'
    
    await update.message.reply_text(
        get_text(user_id, 'welcome'),
        reply_markup=get_main_keyboard(user_id)
    )

async def info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(
        get_text(user_id, 'info_text'),
        reply_markup=get_main_keyboard(user_id)
    )

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(
        get_text(user_id, 'contact_text'),
        reply_markup=get_main_keyboard(user_id)
    )

async def address_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lokatsiya yuborish - yangilangan koordinatalar
    latitude = 41.36972830271923
    longitude = 69.2723819156919
    
    await update.message.reply_location(
        latitude=latitude,
        longitude=longitude
    )

async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ['🇷🇺 Русский', '🇺🇿 O\'zbekcha'],
        ['🇬🇧 English']
    ]
    await update.message.reply_text(
        TRANSLATIONS['ru']['select_lang'],
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def social_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(
        "📱 Instagram: https://instagram.com/fitness_club_uz",
        reply_markup=get_main_keyboard(user_id)
    )

async def start_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(
        get_text(user_id, 'enter_name'),
        reply_markup=ReplyKeyboardRemove()
    )
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    context.user_data['name'] = update.message.text
    
    keyboard = [[KeyboardButton(get_text(user_id, 'share_phone'), request_contact=True)]]
    await update.message.reply_text(
        get_text(user_id, 'share_phone'),
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if update.message.contact:
        context.user_data['phone'] = update.message.contact.phone_number
    else:
        context.user_data['phone'] = update.message.text
    
    keyboard = [
        [get_text(user_id, 'pricing'), get_text(user_id, 'swimming')],
        [get_text(user_id, 'fitness'), get_text(user_id, 'group')],
        [get_text(user_id, 'other')]
    ]
    await update.message.reply_text(
        get_text(user_id, 'select_service'),
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return SERVICE

async def get_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.username
    chat_id = update.effective_chat.id
    
    
    user_lang = user_languages.get(user_id, 'ru')
    lang_names = {'ru': 'ru', 'uz': 'uz', 'en': 'en'}
    
    context.user_data['service'] = update.message.text
    
    
    admin_message = f"""📝 New Inquiry (lang: {lang_names[user_lang]})

👤 Name: {context.user_data['name']}
📱 Phone: {context.user_data['phone']}
🏋️ Preference: {context.user_data['service']}
👨‍💼 User: @{user_name if user_name else 'No username'}
🆔 Chat ID: {chat_id}"""
    
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Mark Contacted", callback_data=f"contacted_{chat_id}"),
            InlineKeyboardButton("✔️ Mark Completed", callback_data=f"completed_{chat_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID, 
            text=admin_message,
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Adminга yuborishda xatolik: {e}")
    
    # Userga tasdiqlash
    await update.message.reply_text(
        get_text(user_id, 'booking_sent'),
        reply_markup=get_main_keyboard(user_id)
    )
    
    return ConversationHandler.END

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data.startswith('contacted_'):
        
        new_text = query.message.text + "\n\n✅ Status: Contacted"
        await query.edit_message_text(
            text=new_text,
            reply_markup=None
        )
    
    elif data.startswith('completed_'):
        
        new_text = query.message.text + "\n\n✔️ Status: Completed"
        await query.edit_message_text(
            text=new_text,
            reply_markup=None
        )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(
        get_text(user_id, 'cancelled'),
        reply_markup=get_main_keyboard(user_id)
    )
    return ConversationHandler.END

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    # Til tanlash
    if text == '🇷🇺 Русский':
        user_languages[user_id] = 'ru'
        await update.message.reply_text(
            get_text(user_id, 'lang_changed'),
            reply_markup=get_main_keyboard(user_id)
        )
    elif text == '🇺🇿 O\'zbekcha':
        user_languages[user_id] = 'uz'
        await update.message.reply_text(
            get_text(user_id, 'lang_changed'),
            reply_markup=get_main_keyboard(user_id)
        )
    elif text == '🇬🇧 English':
        user_languages[user_id] = 'en'
        await update.message.reply_text(
            get_text(user_id, 'lang_changed'),
            reply_markup=get_main_keyboard(user_id)
        )
    # Menu tugmalari
    elif text in [TRANSLATIONS['ru']['info'], TRANSLATIONS['uz']['info'], TRANSLATIONS['en']['info']]:
        await info_handler(update, context)
    elif text in [TRANSLATIONS['ru']['contact'], TRANSLATIONS['uz']['contact'], TRANSLATIONS['en']['contact']]:
        await contact_handler(update, context)
    elif text in [TRANSLATIONS['ru']['address'], TRANSLATIONS['uz']['address'], TRANSLATIONS['en']['address']]:
        await address_handler(update, context)
    elif text in [TRANSLATIONS['ru']['language'], TRANSLATIONS['uz']['language'], TRANSLATIONS['en']['language']]:
        await language_handler(update, context)
    elif text in [TRANSLATIONS['ru']['social'], TRANSLATIONS['uz']['social'], TRANSLATIONS['en']['social']]:
        await social_handler(update, context)

def main():
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Conversation handler for booking
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(
            filters.Regex(f"^({TRANSLATIONS['ru']['booking']}|{TRANSLATIONS['uz']['booking']}|{TRANSLATIONS['en']['booking']})$"),
            start_booking
        )],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler((filters.CONTACT | filters.TEXT) & ~filters.COMMAND, get_phone)],
            SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_service)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    # Botni ishga tushirish
    print("Bot ishga tushdi...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

