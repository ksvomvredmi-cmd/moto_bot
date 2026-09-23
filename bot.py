import asyncio
import http.server
import os
import threading
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)
from aiohttp import web

# --- Міні-сервер для утримання порту Railway ---
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
TOKEN = "8895105299:AAEYm9Qsb8K-gZrSPTBxwrUb56sTKkHp9cY"
TARGET_CHAT_ID = -1004344737401  # ID вашей группы
ADMIN_ID = 1087968824

bot = Bot(token=TOKEN)
dp = Dispatcher()

ALLOWED_TYPES = {"text", "photo", "video", "video_note", "voice", "document"}
user_cooldowns = {}
COOLDOWN_TIME = 5

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Почати 🏍")]], resize_keyboard=True
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


# --- Обработчик для пересылки сообщений в группу ---
@dp.message(F.chat.type == "private")
async def forward_to_group(message: Message):
  if message.from_user.id == ADMIN_ID:
    return  # Админа можно исключить или обрабатывать отдельно, если нужно

  if message.content_type not in ALLOWED_TYPES:
    return

  try:
    # Пересылаем сообщение в целевой чат (группу)
    await bot.copy_message(
        chat_id=TARGET_CHAT_ID,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
    )
    await message.answer("✅ Ваше повідомлення надіслано в спільноту!")
  except Exception as e:
    print(f"Помилка при пересиланні: {e}")
    await message.answer("❌ Сталася помилка при надсиланні повідомлення.")


async def main():
  await start_web_server()
  print("Bot started polling...")
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())
