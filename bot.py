import asyncio
import json
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineQuery, InlineQueryResultCachedPhoto

# ==============================
# 👇 ВСТАВЬ ТОКЕН СЮДА
BOT_TOKEN = os.getenv("BOT_TOKEN", "8652922599:AAE61SmbMIs9koGeiQXrXa9GIFRtbdRYaSA")
# ==============================

STORAGE_FILE = "images.json"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def load_images():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    return []


def save_images(images):
    with open(STORAGE_FILE, "w") as f:
        json.dump(images, f)


# --- Принимаем фото ---
@dp.message(F.photo)
async def handle_photo(message: Message):
    images = load_images()
    file_id = message.photo[-1].file_id

    if file_id not in images:
        images.append(file_id)
        save_images(images)
        await message.answer(f"✅ Сохранено! Всего изображений: {len(images)}")
    else:
        await message.answer("⚠️ Это фото уже есть в списке.")


# --- Показываем сколько фото сохранено ---
@dp.message(F.text == "/list")
async def list_images(message: Message):
    images = load_images()
    await message.answer(f"📦 Сохранено изображений: {len(images)}")


# --- Удалить все фото ---
@dp.message(F.text == "/clear")
async def clear_images(message: Message):
    save_images([])
    await message.answer("🗑 Все изображения удалены.")


# --- Инлайн: показываем ВСЕ фото сразу без ввода текста ---
@dp.inline_query()
async def inline_handler(query: InlineQuery):
    images = load_images()
    results = [
        InlineQueryResultCachedPhoto(
            id=str(i),
            photo_file_id=file_id
        )
        for i, file_id in enumerate(images)
    ]
    # Telegram позволяет максимум 50 результатов за раз
    await query.answer(results[:50], cache_time=1, is_personal=True)


async def main():
    print("Бот запущен ✅")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
