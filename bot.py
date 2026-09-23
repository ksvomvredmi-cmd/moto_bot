import asyncio import os import time from aiogram import Bot, Dispatcher, F from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
Вставте ваш токен від @BotFather
TOKEN = "8895105299:AAEYm9Qsb8K-gZrSPTBxwrUb56sTKkHp9cY"
Вставте ID вашого анонімного каналу або групи (має починатися з -100...)
TARGET_CHAT_ID = -1004344737401
Впишіть сюди ваш цифровий Telegram ID (дізнатися можна у @userinfobot)
ADMIN_ID = 1087968824
bot = Bot(token=TOKEN) dp = Dispatcher()
ALLOWED_TYPES = {'text', 'photo', 'video', 'video_note', 'voice', 'document'}
Словник для відстеження часу останнього повідомлення користувача {user_id: timestamp}
user_cooldowns = {}
Гнучкий інтервал антиспаму (у секундах)
Можете змінити за потреби: базовий 10с, при високій активності можна знизити до 5с
COOLDOWN_TIME = 5  # Зменшено до 5 секунд для підтримки високої активності
Головне меню з двома кнопками
main_keyboard = ReplyKeyboardMarkup( keyboard=[ [KeyboardButton(text="Почати 🏍️")], [KeyboardButton(text="📝 Правила спільноти 📝")] ], resize_keyboard=True )
Текст правил спільноти
RULES_TEXT = ( "Спільнота створена в розважальних цілях, вона не несе за собою поганий характер.\n\n" "          🚫 <b>ЗАБОРОНЯЄТЬСЯ</b> 🚫\n\n" "<b>1.</b> Кидати сливи, ЦП, 18+ контент.\n" "<b>2.</b> Заборонено пригнічувати людей.\n" "<b>3.</b> Заборона реклами (дозволена в разі допомоги).\n\n" "⚠️ <i>В разі порушення правил 3 рази вас заблокують!</i>" )
Команда /start
@dp.message(F.text == "/start") async def cmd_start(message: Message): welcome_text = ( f"Привіт, <b>{message.from_user.first_name}</b>! Вітаю у бота спільноти <b>МотоНя</b> 🏍️\n\n" "Обери потрібну кнопку нижче:" ) await message.answer(welcome_text, reply_markup=main_keyboard, parse_mode="HTML")
Кнопка «Почати 🏍️»
@dp.message(F.text == "Почати 🏍️") async def btn_start_action(message: Message): await message.answer( "✊ Готово! Тепер просто надішли мені текст, фото, відео чи кружок, і я анонімно опублікую його в каналі.", reply_markup=main_keyboard )
Кнопка «📝 Правила спільноти 📝»
@dp.message(F.text == "📝 Правила спільноти 📝") async def btn_rules_action(message: Message): await message.answer(RULES_TEXT, parse_mode="HTML", reply_markup=main_keyboard)
Ексклюзивна команда для зупинки бота (тільки для адміна)
@dp.message(F.text == "/stop_bot") async def stop_bot(message: Message): if message.from_user.id == ADMIN_ID: await message.answer("🛑 Бот вимикається за командою адміністратора...", reply_markup=ReplyKeyboardRemove()) os._exit(0) else: await message.answer("⚠️ У вас немає прав на виконання цієї команди.")
Анонімне пересилання з антиспамом для ВСІХ
@dp.message(F.content_type.in_(ALLOWED_TYPES)) async def forward_anonymous(message: Message): # Ігноруємо натискання меню-кнопок if message.text in ["Почати 🏍️", "📝 Правила спільноти 📝"]: return
Python


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
Блокування забороненого контенту
@dp.message(F.content_type.in_({'location', 'sticker', 'contact'})) async def block_unwanted(message: Message): await message.answer("⚠️ Геолокації, стікери та контакти заборонені заради анонімності та безпеки.")
if name == "main": asyncio.run(dp.start_polling(bot))