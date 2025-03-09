import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from logic import start_quiz, check_answer, ask_question

TOKEN = "YOUR-TOKEN"
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    question, keyboard, meme, caption = start_quiz(message.from_user.id)
    if question:
        await message.answer(question, reply_markup=keyboard)
    elif meme:
        await bot.send_photo(message.chat.id, meme, caption=caption)

@dp.message()
async def handle_answer(message: types.Message):
    question, keyboard, meme, caption = check_answer(message.from_user.id, message.text)
    if question:
        await message.answer(question, reply_markup=keyboard)
    elif meme:
        await bot.send_photo(message.chat.id, meme, caption=caption)
    else:
        await message.answer("Неверно! Начинаем заново!")
        await asyncio.sleep(2)
        question, keyboard, _, _ = start_quiz(message.from_user.id)
        await message.answer(question, reply_markup=keyboard)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
