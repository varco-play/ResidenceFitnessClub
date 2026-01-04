# 🏋️ Residence Fitness Club Telegram Bot

Fitness klub uchun ko'p tilli Telegram bot (Rus, O'zbek, Ingliz).

## 🌟 Xususiyatlar

- ✅ 3 til: Русский, O'zbekcha, English
- ✅ Klub haqida ma'lumot
- ✅ Ariza yuborish tizimi
- ✅ Lokatsiya ko'rsatish
- ✅ Admin uchun bildirishnomalar
- ✅ Inline tugmalar bilan holat boshqaruvi

## 📋 Talablar

- Python 3.8+
- python-telegram-bot 20.7

## ⚙️ O'rnatish

### 1. Repozitoriyani klonlash

```bash
git clone https://github.com/varco-play/ResidenceFitnessClub.git
cd ResidenceFitnessClub
```

### 2. Virtual environment yaratish (ixtiyoriy)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

### 3. Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4. Konfiguratsiya

`config.py` fayl yarating va quyidagilarni kiriting:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_ID = YOUR_TELEGRAM_ID
```

**Bot token olish:**
1. [@BotFather](https://t.me/BotFather) ga murojaat qiling
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting
4. Token oling

**Admin ID olish:**
1. [@userinfobot](https://t.me/userinfobot) ga `/start` yuboring
2. O'z ID'ingizni ko'ring

### 5. Botni ishga tushirish

```bash
python bot.py
```

Terminal'da ko'rinadi: `Bot ishga tushdi...`

## 🚀 Deploy qilish

### PythonAnywhere (Bepul)

1. [pythonanywhere.com](https://pythonanywhere.com) ro'yxatdan o'ting
2. Console → Bash:
```bash
git clone https://github.com/varco-play/ResidenceFitnessClub.git
cd ResidenceFitnessClub
pip install -r requirements.txt --user
```
3. `config.py` yarating
4. Botni ishga tushiring: `python bot.py`

### Render.com

1. GitHub repository ulang
2. New → Background Worker
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python bot.py`
5. Environment Variables'ga `BOT_TOKEN` va `ADMIN_ID` qo'shing

## 📱 Bot buyruqlari

- `/start` - Botni ishga tushirish
- `/cancel` - Ariza yuborishni bekor qilish

## 🗂️ Fayl strukturasi

```
ResidenceFitnessClub/
│
├── bot.py              # Asosiy bot kodi
├── config.py           # Maxfiy sozlamalar (gitignore)
├── requirements.txt    # Python kutubxonalar
├── .gitignore          # Git ignore fayllar
└── README.md           # Loyiha haqida
```

## 🔒 Xavfsizlik

- ⚠️ `config.py` faylini **hech qachon GitHub'ga joylashtirmang!**
- ⚠️ `.gitignore` da `config.py` borligiga ishonch hosil qiling
- ⚠️ Bot tokenni hech kimga bermang

## 📞 Kontakt

Savollar bo'lsa, issue oching yoki admin bilan bog'laning.

## 📄 Litsenziya

MIT License

---

Made with ❤️ for Residence Fitness Club
