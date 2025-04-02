import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import datetime

TOKEN = "8029649809:AAEmDL6CeuXuBLmCKo8ixNakwGQFdMir-SM"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Хранение текстов ритуалов
morning_text = "Текст утреннего ритуала пока не загружен."
evening_text = "Текст вечернего ритуала пока не загружен."

# Создаем клавиатуру
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Утренний ритуал"))
keyboard.add(KeyboardButton("Вечерний ритуал"))

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет! Я ваш бот. Выберите ритуал:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Утренний ритуал")
async def morning_ritual(message: types.Message):
    await message.answer(morning_text)

@dp.message_handler(lambda message: message.text == "Вечерний ритуал")
async def evening_ritual(message: types.Message):
    await message.answer(evening_text)

async def update_rituals():
    global morning_text, evening_text
    while True:
        now = datetime.datetime.now()
        if now.hour == 21:  # В 21:00 обновляем вечерний ритуал
            evening_text = "Новый текст вечернего ритуала от ИИ."
        elif now.hour == 22:  # В 22:00 обновляем утренний ритуал
            morning_text = "Новый текст утреннего ритуала от ИИ."
        await asyncio.sleep(3600)  # Проверяем раз в час

async def notify_users():
    while True:
        now = datetime.datetime.now()
        if now.hour == 9:  # Отправляем утренний ритуал в 9 утра
            await bot.send_message(YOUR_CHAT_ID, morning_text)
        elif now.hour == 22:  # Отправляем вечерний ритуал в 22 вечера
            await bot.send_message(YOUR_CHAT_ID, evening_text)
        await asyncio.sleep(3600)  # Проверяем раз в час

async def main():
    asyncio.create_task(update_rituals())
    asyncio.create_task(notify_users())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
