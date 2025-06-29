from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)

import config
import prompt


_FLAGS = {
    "EN": "\U0001F1EC\U0001F1E7",
    "RU": "\U0001F1F7\U0001F1FA",
    "PL": "\U0001F1F5\U0001F1F1"
}


async def translate(text: str) -> str:
    translations = await prompt.translate(text)
    # Simulate an async call to OpenAI
    return f"\n".join(f"{_FLAGS[lang]}: {text}" for lang, text in translations.items())


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello GTR! I'll be translating your messages to English, Polish and Russian automatically!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    original_text = update.message.text
    translated = await translate(original_text)
    await update.message.reply_text(
        translated,
        reply_to_message_id=update.message.message_id
    )


app = ApplicationBuilder().token(config.BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


webhook_app = FastAPI()


@webhook_app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, app.bot)
    await app.process_update(update)
    return {"ok": True}


@webhook_app.on_event("startup")
async def register_webhook():
    await app.bot.set_webhook(url=f"{config.APP_URL}/webhook")


def main():
    app.run_polling()


if __name__ == "__main__":
    main()
