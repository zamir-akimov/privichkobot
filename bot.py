import logging
import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, JobQueue

# Вставьте свой токен бота
TOKEN = "YOUR_BOT_TOKEN_HERE"

# Тексты ритуалов
MORNING_TEXT = "Доброе утро! Вот ваш утренний ритуал. ☀️"
EVENING_TEXT = "Добрый вечер! Вот ваш вечерний ритуал. 🌙"

# Настройка кнопок
keyboard = [
    [KeyboardButton("Утренний ритуал"), KeyboardButton("Вечерний ритуал")],
    [KeyboardButton("Создать привычку")]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Словарь для хранения привычек пользователей
user_habits = {}

# Настройка логирования
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

def start(update: Update, context: CallbackContext) -> None:
    """Приветственное сообщение"""
    update.message.reply_text("Привет! Выберите ритуал или создайте привычку:", reply_markup=markup)

def handle_message(update: Update, context: CallbackContext) -> None:
    """Обработчик кнопок"""
    text = update.message.text
    chat_id = update.message.chat_id

    if text == "Утренний ритуал":
        update.message.reply_text(MORNING_TEXT)
    elif text == "Вечерний ритуал":
        update.message.reply_text(EVENING_TEXT)
    elif text == "Создать привычку":
        update.message.reply_text("Введите описание привычки:")
        context.user_data["awaiting_habit"] = True
    elif "awaiting_habit" in context.user_data:
        context.user_data["habit_description"] = text
        update.message.reply_text("Введите время для напоминания (в формате ЧЧ:ММ):")
        context.user_data.pop("awaiting_habit")
        context.user_data["awaiting_time"] = True
    elif "awaiting_time" in context.user_data:
        try:
            habit_time = datetime.datetime.strptime(text, "%H:%M").time()
            user_habits[chat_id] = (context.user_data["habit_description"], habit_time)
            update.message.reply_text(f"Привычка сохранена! Бот напомнит вам в {habit_time}. ✅")
            context.user_data.pop("awaiting_time")
            schedule_habit_reminder(context, chat_id, context.user_data["habit_description"], habit_time)
        except ValueError:
            update.message.reply_text("Некорректный формат времени. Введите в формате ЧЧ:ММ.")

def schedule_habit_reminder(context: CallbackContext, chat_id: int, habit_description: str, habit_time: datetime.time):
    """Запускаем напоминание"""
    now = datetime.datetime.now()
    reminder_datetime = datetime.datetime.combine(now.date(), habit_time)
    if reminder_datetime < now:
        reminder_datetime += datetime.timedelta(days=1)

    delay = (reminder_datetime - now).total_seconds()
    context.job_queue.run_once(send_habit_reminder, delay, context={"chat_id": chat_id, "habit_description": habit_description})

def send_habit_reminder(context: CallbackContext):
    """Отправляем напоминание пользователю"""
    job_data = context.job.context
    context.bot.send_message(chat_id=job_data["chat_id"], text=f"🔔 Напоминание: {job_data['habit_description']}")

def main():
    """Запуск бота"""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    job_queue = updater.job_queue

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
