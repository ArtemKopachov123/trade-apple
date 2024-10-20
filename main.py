from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton
import asyncio
#from create_bot import bot, dp #путь к файлу с созданием бота
#from handlers.start import start_router

TOKEN = '7946703986:AAHftunfdRkOy5zN2UrM-wxi2EUeZRNfrB4'  # Замените на ваш токен
bot = Bot(TOKEN)
dp = Dispatcher()
start_router = Router()


form_stage = "start"

model = ""
photos = []
memory = ""
battery = ""
price = ""
condition = ""
username = ""
city = ""
details = ""

@start_router.message(Command('start'))
async def command_start(message: Message):
    global form_stage
    form_stage = "start"
    await message.answer(
        """*👋 Привет! 👋*\n
*Хочешь продать свой iPhone? Отлично!*\n
*Заполни форму ниже, чтобы разместить объявление в* [канале](https://t.me/tradeapplepromax).\n
*Гарант/менеджер: @mgmttradeapple 🛡*\n
👇 *Начни с модели телефона:*""", disable_web_page_preview=True, parse_mode='MarkDown')

@start_router.message()
async def command_process_message(message: Message):
    global form_stage, model, memory, battery, photos, price, condition, username, city, details

    if form_stage == "start":
        model = message.text
        form_stage = "memory"
        await message.answer("*👌 Отлично! Теперь скажи, сколько памяти у телефона?*", parse_mode='MarkDown')

    elif form_stage == "memory":
        memory = message.text
        form_stage = "battery"
        await message.answer("*🔋 А как с состоянием аккумулятора?*", parse_mode='MarkDown')

    elif form_stage == "battery":
        battery = message.text
        form_stage = "photos"
        await message.answer("*📸 Теперь отправьте фотографии смартфона*", parse_mode='MarkDown')

    elif form_stage == "photos":
        if message.photo:
            photos.append(message.photo[-1].file_id)  # Сохраняем последнюю версию фотографии (самую качественную)
            form_stage = "price"
            await message.answer("*💰 Какая цена?*", parse_mode='Markdown')
        else:
            await message.answer("Пожалуйста, отправьте фото")

    elif form_stage == "price":
        price = message.text
        form_stage = "condition"
        await message.answer("*🔍 Внешний вид телефона*", parse_mode='MarkDown')

    elif form_stage == "condition":
        condition = message.text
        form_stage = "username"
        await message.answer("*📞 Введите ваш юзернейм в Telegram*", parse_mode='MarkDown')

    elif form_stage == "username":
        username = message.text
        form_stage = "city"
        await message.answer("*🏙 В каком городе вы находитесь?*", parse_mode='MarkDown')

    elif form_stage == "city":
        city = message.text
        form_stage = "details"
        await message.answer("""*📋 Есть ли какие-то дополнительные нюансы?*\n
(комплект, вскрывался ли)""", parse_mode='MarkDown')

    elif form_stage == "details":
        details = message.text
        await message.answer("""*Спасибо! Ваша заявка получена! 🤝*\n
*Новая заявка - /start*""", parse_mode='MarkDown')

        chats_id = ['1797047165', '7213857743', '1090086980']
        try:
            for chat_id in chats_id:
              # Отправляем информацию о заявке
              await bot.send_message(
                  chat_id,
                  text=f"Новая заявка:\n"
                  f"Модель: {model}\n"
                  f"Память: {memory}\n"
                  f"Аккумулятор: {battery}\n"
                  f"Цена: {price}\n"
                  f"Состояние: {condition}\n"
                  f"Юзернейм: {username}\n"
                  f"Город: {city}\n"
                  f"Нюансы: {details}"
              )
              # Отправляем фотографии
              for photo_id in photos:
                  await bot.send_photo(chat_id, photo_id)
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")

async def main():
    dp.include_router(start_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())