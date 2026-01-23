# Fitness Club Telegram Bot 🏋️

A multi-language Telegram bot for fitness club management with booking system.

## Features ✨

- 🌐 Multi-language support (Russian, Uzbek, English)
- 📝 Booking system with admin notifications
- 📍 Location sharing
- 👥 User-friendly keyboard interface
- 📱 Contact sharing capability

## Quick Deploy to Render 🚀

### Step 1: Get Your Credentials

1. **Get Bot Token from BotFather:**
   - Open Telegram and search for `@BotFather`
   - Send `/newbot` and follow instructions
   - Copy the token (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

2. **Get Your Admin ID:**
   - Search for `@userinfobot` on Telegram
   - Send `/start`
   - Copy your ID (format: `123456789`)

### Step 2: Deploy to Render

1. **Fork or Upload to GitHub:**
   - Create a new repository on GitHub
   - Upload all these files to your repository

2. **Connect to Render:**
   - Go to [render.com](https://render.com) and sign up
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure Service:**
   - **Name:** fitness-telegram-bot (or your choice)
   - **Region:** Select closest to you
   - **Branch:** main
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python tbot.py`
   - **Instance Type:** Free

4. **Add Environment Variables:**
   
   Click "Add Environment Variable" and add these two:
   
   - **Key:** `BOT_TOKEN`  
     **Value:** Your token from BotFather
   
   - **Key:** `ADMIN_ID`  
     **Value:** Your Telegram user ID

5. **Deploy:**
   - Click "Create Web Service"
   - Wait 2-5 minutes for deployment
   - Check logs for "✅ Bot running on Render"

### Step 3: Test Your Bot

1. Open Telegram
2. Search for your bot username
3. Send `/start`
4. Test all menu options

## Commands 💬

- `/start` - Start the bot and show main menu
- `/cancel` - Cancel current booking process

## Menu Options 📋

- **ℹ️ Info** - View club information
- **📝 Booking** - Make a new booking
- **📞 Contact** - Get contact information
- **📍 Address** - View location on map
- **🌐 Language** - Change language
- **📱 Social** - Social media links

## Booking Flow 📝

1. User clicks "📝 Booking"
2. Enters full name
3. Shares phone number
4. Selects service type
5. Admin receives notification

## Customization 🎨

### Change Club Information

Edit in `tbot.py`:
```python
"info_text": "💪 Your Fitness Club Name\n\n⏰ Your Hours\n..."
"contact_text": "📞 Phone: +998xxxxxxxxx"
```

### Change Location

Edit coordinates in `tbot.py`:
```python
await update.message.reply_location(41.3697283, 69.2723819)
```

### Add More Languages

Add new language in `TRANSLATIONS` dictionary in `tbot.py`.

## Troubleshooting 🔧

### Bot not responding?
- Check Render logs for errors
- Verify `BOT_TOKEN` is correct
- Ensure bot is not running elsewhere

### Admin not receiving bookings?
- Verify `ADMIN_ID` is correct
- Start a conversation with bot first

### Deployment failed?
- Check all files are uploaded
- Verify `requirements.txt` exists
- Review build logs in Render

## Local Development 💻

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file:
   ```
   BOT_TOKEN=your_token_here
   ADMIN_ID=your_id_here
   ```
4. Run: `python tbot.py`

## File Structure 📁

```
.
├── tbot.py              # Main bot code
├── requirements.txt     # Python dependencies
├── render.yaml          # Render configuration
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Support 💬

For issues or questions:
- Check Render logs first
- Review Telegram Bot API documentation
- Ensure all environment variables are set correctly

## License 📄

This project is open source and available for modification.

---

**Made with ❤️ for Residence Fitness Club**
