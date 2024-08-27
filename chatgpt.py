import os
import cohere
import asyncio
from telegram import Update, ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import nest_asyncio

nest_asyncio.apply()

cohere_api_key = 'v0TqIJO3L0k5J74Jcn6waSWstOqFJHmkG18aOzEi'
co = cohere.Client(cohere_api_key)

telegram_token = '7406870442:AAEcOkcBKC2FOP17s4BuY87UDmAA884NIfI'
webhook_url = os.getenv('WEBHOOK_URL', 'https://chatgpt-bot-9wty.onrender.com')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет сообщение при команде /start."""
    await update.message.reply_text('Привет! Я бот, использующий Cohere API. Напишите мне что-нибудь, и я отвечу!')


async def generate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        # Показать действие "печатает..."
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

        # Генерация текста с помощью Cohere
        response = co.generate(
            model='command-xlarge-nightly',
            prompt=user_message,
            max_tokens=1500,
            temperature=0.7
        )
        generated_text = response.generations[0].text.strip()

        await update.message.reply_text(generated_text)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        await update.message.reply_text("Извините, произошла ошибка при обработке вашего запроса.")


async def main():
    application = Application.builder().token(telegram_token).build()

    # Настройка Webhook
    await application.bot.set_webhook(url=webhook_url)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_text))

    # Запуск Webhook
    await application.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        url_path="",
        webhook_url=webhook_url
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
