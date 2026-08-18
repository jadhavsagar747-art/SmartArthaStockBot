import os
import requests

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
UPSTOX_TOKEN = os.getenv("UPSTOX_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 Welcome to SmartArthaStockBot\n\n"
        "Commands:\n"
        "/price AXISBANK\n"
        "/price ICICIBANK\n"
        "/price HDFCBANK"
    )


def find_instrument(symbol):
    url = "https://api.upstox.com/v2/instruments/search"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {UPSTOX_TOKEN}"
    }

    params = {
        "query": symbol,
        "exchanges": "NSE",
        "segments": "EQ",
        "records": 10
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    for stock in data.get("data", []):
        if stock.get("trading_symbol", "").upper() == symbol.upper():
            return stock["instrument_key"]

    return None


def get_price(symbol):
    instrument_key = find_instrument(symbol)

    if not instrument_key:
        return None

    url = "https://api.upstox.com/v3/market-quote/ltp"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {UPSTOX_TOKEN}"
    }

    params = {
        "instrument_key": instrument_key
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()["data"]

    quote = next(iter(data.values()))

    return {
        "price": quote.get("last_price"),
        "previous_close": quote.get("cp"),
        "volume": quote.get("volume")
    }


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Please enter a stock symbol.\n\n"
            "Example:\n"
            "/price AXISBANK"
        )
        return

    symbol = context.args[0].upper()

    try:
        result = get_price(symbol)

        if result is None:
            await update.message.reply_text(
                f"❌ Stock {symbol} not found."
            )
            return

        current_price = result["price"]
        previous_close = result["previous_close"]
        volume = result["volume"]

        if previous_close:
            change = current_price - previous_close
            change_percent = (
                change / previous_close
            ) * 100
        else:
            change = 0
            change_percent = 0

        message = (
            f"📊 SMART ARTHA STOCK\n\n"
            f"Stock: {symbol}\n"
            f"LTP: ₹{current_price:.2f}\n"
            f"Previous Close: ₹{previous_close:.2f}\n"
            f"Change: ₹{change:.2f}\n"
            f"Change: {change_percent:.2f}%\n"
            f"Volume: {volume:,}"
        )

        await update.message.reply_text(message)

    except Exception as error:
        print(error)

        await update.message.reply_text(
            "⚠️ Unable to fetch stock data."
        )


def main():

    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN is missing")

    if not UPSTOX_TOKEN:
        raise ValueError("UPSTOX_TOKEN is missing")

    app = Application.builder().token(
        TELEGRAM_TOKEN
    ).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("price", price)
    )

    print("SmartArthaStockBot running...")

    app.run_polling()


if __name__ == "__main__":
    main()