import os
import cohere
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

cohere_api_key = 'pdmEdFBDZqFYH9ljBReMM4VzSPIOwij2bJZNiPwv'
co = cohere.Client(cohere_api_key)

telegram_token = '7406870442:AAEcOkcBKC2FOP17s4BuY87UDmAA884NIfI'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет сообщение при команде /start."""
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

def main():
    application = Application.builder().token(telegram_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_text))

    application.run_polling()

if __name__ == '__main__':
    main()