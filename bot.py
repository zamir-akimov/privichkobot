
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = "8029649809:AAEmDL6CeuXuBLmCKo8ixNakwGQFdMir-SM"

# Тексты для кнопок
morning_text = "Доброе утро! Вот ваш утренний ритуал."
evening_text = "Добрый вечер! Вот ваш вечерний ритуал."

# Создаем клавиатуру
keyboard = [[KeyboardButton("Утренний ритуал"), KeyboardButton("Вечерний ритуал")]]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привет! Выберите ритуал:", reply_markup=markup)

def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text == "Утренний ритуал":
        update.message.reply_text(morning_text)
    elif text == "Вечерний ритуал":
        update.message.reply_text(evening_text)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
