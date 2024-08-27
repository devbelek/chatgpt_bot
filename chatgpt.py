import asyncio
import os
import cohere
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


cohere_api_key = 'pdmEdFBDZqFYH9ljBReMM4VzSPIOwij2bJZNiPwv'
co = cohere.Client(cohere_api_key)

telegram_token = '7406870442:AAEcOkcBKC2FOP17s4BuY87UDmAA884NIfI'
webhook_url = os.getenv('WEBHOOK_URL', 'https://chatgpt-bot-9wty.onrender.com')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я бот, использующий Cohere API. Напишите мне что-нибудь, и я отвечу!')


async def generate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = co.generate(
            model='command-xlarge-nightly',
            prompt=user_message,
            max_tokens=300,
            temperature=0.7
        )
        generated_text = response.generations[0].text.strip()

        await update.message.reply_text(generated_text)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        await update.message.reply_text("Извините, произошла ошибка при обработке вашего запроса.")


async def main():
    application = Application.builder().token(telegram_token).build()


    await application.bot.set_webhook(url=webhook_url)


    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_text))

    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        url_path="",
        webhook_url=webhook_url
    )

async def main():
    application = Application.builder().token(telegram_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_text))

    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.updater.idle()

if __name__ == '__main__':
    asyncio.run(main())
