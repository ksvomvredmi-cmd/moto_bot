import asyncio 
import os 
import time 
from aiogram import Bot, Dispatcher, F 
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
TOKEN = "8895105299:AAEYm9Qsb8K-gZrSPTBxwrUb56sTKkHp9cY"
TARGET_CHAT_ID = -1004344737401
ADMIN_ID = 1087968824
bot = Bot(token=TOKEN) 
dp = Dispatcher()
ALLOWED_TYPES = {'text', 'photo', 'video', 'video_note', 'voice', 'document'}
{user_id: timestamp}
user_cooldowns = {}
COOLDOWN_TIME = 5  # Зменшено до 5 секунд для підтримки високої активності
main_keyboard = ReplyKeyboardMarkup( keyboard=[ [KeyboardButton(text="Почати 🏍️")], [KeyboardButton(text="📝 Правила спільноти 📝")] ], resize_keyboard=True )
RULES_TEXT = ( "Спільнота створена в розважальних цілях, вона не несе за собою поганий характер.\n\n" "          🚫 <b>ЗАБОРОНЯЄТЬСЯ</b> 🚫\n\n" "<b>1.</b> Кидати сливи, ЦП, 18+ контент.\n" "<b>2.</b> Заборонено пригнічувати людей.\n" "<b>3.</b> Заборона реклами (дозволена в разі допомоги).\n\n" "⚠️ <i>В разі порушення правил 3 рази вас заблокують!</i>" )
@dp.message(F.text == "/start") 
async def cmd_start(message: Message): welcome_text = ( f"Привіт, <b>{message.from_user.first_name}</b>! Вітаю у бота спільноти <b>МотоНя</b> 🏍️\n\n" "Обери потрібну кнопку нижче:" ) 
await message.answer(welcome_text, reply_markup=main_keyboard, parse_mode="HTML")

@dp.message(F.text == "Почати 🏍️") 
async def btn_start_action(message: Message): 
    await message.answer( "✊ Готово! Тепер просто надішли мені текст, фото, відео чи кружок, і я анонімно опублікую його в каналі.", reply_markup=main_keyboard )

@dp.message(F.text == "📝 Правила спільноти 📝") 
async def btn_rules_action(message: Message): 
    await message.answer(RULES_TEXT, parse_mode="HTML", reply_markup=main_keyboard)

@dp.message(F.text == "/stop_bot") 
async def stop_bot(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("🛑 Бот вимикається за командою адміністратора...", reply_markup=ReplyKeyboardRemove()) 
        os._exit(0) 
    else: 
        await message.answer("⚠️ У вас немає прав на виконання цієї команди.")

@dp.message(F.content_type.in_(ALLOWED_TYPES))
async def forward_anonymous(message: Message): 
    if message.text in ["Почати 🏍️", "📝 Правила спільноти 📝"]: return
    user_id = message.from_user.id
    current_time = time.time()

# Адміністратора звільняємо від обмежень антиспаму, щоб він міг постити миттєво
if user_id != ADMIN_ID:
    last_time = user_cooldowns.get(user_id, 0)
    time_diff = current_time - last_time

    if time_diff < COOLDOWN_TIME:
        wait_sec = int(COOLDOWN_TIME - time_diff) + 1
        await message.answer(f"⏳ Зачекай ще {wait_sec} сек. перед відправкою наступного повідомлення (захист від спаму).")
        return

    # Оновлюємо час останнього повідомлення для цього користувача
    user_cooldowns[user_id] = current_time

try:
    # Копіюємо контент у канал анонімно
    await message.copy_to(chat_id=TARGET_CHAT_ID)
    await message.answer("✅ Ваше повідомлення анонімно опубліковано в групі! 🏍️")
except Exception:
    await message.answer("⚠️ Сталася помилка при відправці.")

@dp.message(F.content_type.in_({'location', 'sticker', 'contact'})) 
async def block_unwanted(message: Message): 
    await message.answer("⚠️ Геолокації, стікери та контакти заборонені заради анонімності та безпеки.")
if name == "main": 
                asyncio.run(dp.start_polling(bot))
