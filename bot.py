import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8944557353:AAGvGfGLB7_m4NjBhqvSLVzg7qX3ButdcFA"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

players = {}

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("🏰 Моя страна"), KeyboardButton("🌍 Список стран"))
main_menu.add(KeyboardButton("⚙️ Производство"))

prod_menu = ReplyKeyboardMarkup(resize_keyboard=True)
prod_menu.add(KeyboardButton("🍗 Еда"), KeyboardButton("🔩 Железо"))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in players:
        players[user_id] = {
            "name": None, "gold": 1000, "food": 500,
            "iron": 300, "citizens": 50, "power": 500
        }
        await message.answer("Введи название страны:")
    else:
        await message.answer("Твоя страна уже есть!", reply_markup=main_menu)

@dp.message_handler()
async def handle(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    if user_id in players and players[user_id]["name"] is None:
        players[user_id]["name"] = text
        await message.answer(f"Страна {text} создана!", reply_markup=main_menu)
        return

    if text == "🏰 Моя страна":
        p = players[user_id]
        await message.answer(
            f"{p['name']}\n💰 Золото: {p['gold']}\n🍗 Еда: {p['food']}\n🔩 Железо: {p['iron']}\n👥 Граждане: {p['citizens']}\n⚔️ Сила: {p['power']}"
        )
    elif text == "⚙️ Производство":
        await message.answer("Выбери ресурс:", reply_markup=prod_menu)
    elif text == "🍗 Еда":
        players[user_id]["food"] += 50
        await message.answer("+50 еды", reply_markup=main_menu)
    elif text == "🔩 Железо":
        players[user_id]["iron"] += 30
        await message.answer("+30 железа", reply_markup=main_menu)
    else:
        await message.answer("Используй кнопки", reply_markup=main_menu)

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp)
