import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from googletrans import Translator

API_TOKEN = 'YOUR_BOT_API_TOKEN'

# Logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Initialize Google Translator
translator = Translator()

# Function to translate text
def translate_text(text, src_lang, dest_lang):
    try:
        result = translator.translate(text, src=src_lang, dest=dest_lang)
        return result.text
    except Exception as e:
        return f"Xato: {str(e)}"

# Command handler
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Salom! Tarjima qilish uchun quyidagi formatni ishlating:\n"
        "til1-til2 matn\n"
        "Masalan: uz-ru Salom, qanday yordam bera olishim mumkin?\n"
        "Qo'llab-quvvatlanadigan tillar: uz (O'zbek), ru (Rus), ar (Arab), en (Ingliz)"
    )

@dp.message_handler()
async def translate_message(message: types.Message):
    try:
        text = message.text.strip()
        if '-' not in text:
            raise ValueError("Noto'g'ri format. To'g'ri format: til1-til2 matn")

        parts = text.split(' ', 1)
        if len(parts) != 2:
            raise ValueError("Noto'g'ri format. To'g'ri format: til1-til2 matn")

        lang_pair, content = parts
        src_lang, dest_lang = lang_pair.split('-')

        # Validate language codes
        valid_languages = {'uz': 'uz', 'ru': 'ru', 'ar': 'ar', 'en': 'en'}
        if src_lang not in valid_languages or dest_lang not in valid_languages:
            raise ValueError("Noto'g'ri til kodi. Qo'llab-quvvatlanadigan tillar: uz, ru, ar, en.")

        src_lang_code = valid_languages[src_lang]
        dest_lang_code = valid_languages[dest_lang]

        result = translate_text(content, src_lang_code, dest_lang_code)
        await message.reply(result)
    except ValueError as e:
        await message.reply(f"Xato: {str(e)}")
    except Exception as e:
        await message.reply(f"Xato: {str(e)}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
