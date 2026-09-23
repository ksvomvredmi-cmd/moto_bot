import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)
from aiohttp import web

# --- Налаштування веб-сервера для Railway ---
PORT = int(os.environ.get("PORT", 8080))


async def handle(request):
  return web.Response(text="Bot is running!")


async def start_web_server():
  app = web.Application()
  app.router.add_get("/", handle)
  runner = web.AppRunner(app)
  await runner.setup()
  site = web.TCPSite(runner, "0.0.0.0", PORT)
  await site.start()
  print(f"Web server started on port {PORT}")


# --- Налаштування бота ---
TOKEN = "8895105299:AAEyM9Qsb8K-gzrSPTBxwrUb56sTKkhP9cY"
TARGET_CHAT_ID = -1004344737401
ADMIN_ID = 1087968824

bot = Bot(token=TOKEN)
dp = Dispatcher()

ALLOWED_TYPES = {"text", "photo", "video", "video_note", "voice", "document"}
user_cooldowns = {}
COOLDOWN_TIME = 5

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Почати 🏍")]], resize_keyboard=True
)

RULES_TEXT = (
    "Спільнота створена в розважальних цілях, вона не несе за собою поганий"
    " характер."
)


@dp.message(F.text == "/start")
async def cmd_start(message: Message):
  welcome_text = (
      f"Привіт, <b>{message.from_user.first_name}</b>! Вітаю у бота спільноти"
      " <b>МотоНя</b>"
  )
  await message.answer(
      welcome_text, reply_markup=main_keyboard, parse_mode="HTML"
  )


@dp.message(F.text == "Почати 🏍")
async def btn_start_action(message: Message):
  await message.answer(
      "🟢 Готово! Тепер просто надійшли мені текст, фото, відео чи кружок,"
  )


async def main():
  # Запускаємо веб-сервер та поллінг бота паралельно
  await start_web_server()
  print("Bot started polling...")
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())
