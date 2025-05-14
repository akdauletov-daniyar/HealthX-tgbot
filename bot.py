import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import openai

# Загрузка переменных окружения
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация OpenAI
openai.api_key = OPENAI_API_KEY

# Список пользователей для напоминаний
users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user_id = update.effective_user.id
    users.add(user_id)
    await update.message.reply_text("Привет! Я бот для диагностики. Отправь мне симптомы, и я помогу определить диагноз.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text("Отправь мне симптомы, например: 'головная боль, боль в глазу'.")

async def diagnose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик сообщений с симптомами"""
    symptoms = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты - медицинский ассистент. На основе симптомов определи список возможных диагнозов, дай советы по лечению и список лекарств."},
                {"role": "user", "content": f"Симптомы: {symptoms}"}
            ]
        )
        diagnosis = response.choices[0].message.content
        await update.message.reply_text(diagnosis)
    except Exception as e:
        logger.error(f"Ошибка при запросе к OpenAI: {e}")
        await update.message.reply_text("Произошла ошибка при обработке запроса.")

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Отправка еженедельных напоминаний"""
    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text="Не забудьте проверить свое здоровье!")
        except Exception as e:
            logger.error(f"Ошибка при отправке напоминания пользователю {user_id}: {e}")

def main():
    """Запуск бота"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, diagnose))

    # Настройка планировщика для еженедельных напоминаний
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_reminder, CronTrigger(day_of_week='mon', hour=10, minute=0), args=[application])
    scheduler.start()

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main() 