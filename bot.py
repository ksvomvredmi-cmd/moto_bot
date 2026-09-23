import asyncio
import http.server
import os
import threading
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

# --- Міні-сервер для утримання порту Railway ---
PORT = int(os.environ.get("PORT", 8080))


class SimpleHandler(http.server.BaseHTTPRequestHandler):

  def do_GET(self):
    self.send_response(200)
    self.end_headers()
    self.wfile.write(b"Bot is running!")

  def log_message(self, format, *args):
    pass


def run_http_server():
  server = http.server.HTTPServer(("0.0.0.0", PORT), SimpleHandler)
  server.serve_forever()


# Запускаємо веб-сервер у фоновому потоці
threading.Thread(target=run_http_server, daemon=True).start()

# --- Налаштування твого бота ---
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


if __name__ == "__main__":
  asyncio.run(dp.start_polling(bot))
