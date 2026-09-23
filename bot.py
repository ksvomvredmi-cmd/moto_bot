import asyncio
import http.server
import os
import threading
import time
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
TOKEN = "8895105299:AAEyM9Qsb8K-gzrSPTBxwrUb56sTKkhP9cY"
TARGET_CHAT_ID = -1004344737401
ADMIN_ID = 1087968824

bot = Bot(token=TOKEN)
dp = Dispatcher()

ALLOWED_TYPES = {"text", "photo", "video", "video_note", "voice", "document"}
user_cooldowns = {}
COOLDOWN_TIME = 5

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Почати 🏍")],
        [KeyboardButton(text="📖 Правила спільноти")],
    ],
    resize_keyboard=True,
)

RULES_TEXT = (
    "Спільнота створена в розважальних цілях, вона не несе за собою поганий"
    " характер.\n\n"
    "Будьте чемними та поважайте інших учасників!"
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
      " і я перешлю його анонімно у спільноту.",
      reply_markup=main_keyboard,
  )


@dp.message(F.text == "📖 Правила спільноти")
async def btn_rules_action(message: Message):
  await message.answer(RULES_TEXT, reply_markup=main_keyboard)


# --- Захист від спаму та пересилання повідомлень ---
@dp.message(F.chat.type == "private")
async def forward_to_group(message: Message):
  if message.from_user.id == ADMIN_ID:
    return

  if message.content_type not in ALLOWED_TYPES:
    return

  current_time = time.time()
  last_time = user_cooldowns.get(message.from_user.id, 0)

  if current_time - last_time < COOLDOWN_TIME:
    left_time = int(COOLDOWN_TIME - (current_time - last_time))
    await message.answer(
        f"⏳ Будь ласка, зачекайте ще {left_time} сек. перед надсиланням"
        " наступного повідомлення."
    )
    return

  user_cooldowns[message.from_user.id] = current_time

  try:
    await bot.copy_message(
        chat_id=TARGET_CHAT_ID,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
    )
    await message.answer("✅ Ваше повідомлення анонімно надіслано в спільноту!")
  except Exception as e:
    print(f"Помилка при пересиланні: {e}")
    await message.answer("❌ Сталася помилка при надсиланні повідомлення.")


async def main():
  await start_web_server()
  print("Bot started polling...")
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())
