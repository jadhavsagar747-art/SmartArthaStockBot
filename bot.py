import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 Welcome to SmartArtha Stock Bot!\n\n"
        "Your stock analysis bot is online.\n\n"
        "Available commands:\n"
        "/start - Start SmartArtha\n"
        "/help - Show commands\n"
        "/watchlist - Show SmartArtha watchlist"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 SmartArtha Commands\n\n"
        "/start\n"
        "/watchlist\n"
        "/help"
    )

async def watchlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📈 SmartArtha Watchlist\n\n"
        "HDFC Bank\n"
        "ICICI Bank\n"
        "Reliance\n"
        "L&T\n"
        "Bharti Airtel\n"
        "SBI\n"
        "Axis Bank\n"
        "Sun Pharma\n"
        "ITC\n"
        "M&M\n\n"
        "More stocks will be added soon."
    )

def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("watchlist", watchlist))

    print("SmartArtha Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
