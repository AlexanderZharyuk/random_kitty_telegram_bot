from config import BOT_TOKEN
import logging
from aiogram import Bot, Dispatcher, executor, types
import requests


logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
URL = 'https://api.thecatapi.com/v1/images/search'


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    response = requests.get(URL)
    data = response.json()
    kitty_photo = data[0]['url']
    button = types.InlineKeyboardButton('One more kitty', callback_data='one_more_kitty')
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(button)
    await bot.send_photo(message.from_user.id, photo=kitty_photo, caption="LEEET'S GO", reply_markup=keyboard)


@dp.callback_query_handler(text='one_more_kitty')
async def one_more_kitty(call: types.CallbackQuery):
    button = types.InlineKeyboardButton('One more kitty', callback_data='one_more_kitty')
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(button)

    response = requests.get(URL)
    data = response.json()
    kitty_photo = data[0]['url']

    await bot.send_photo(call.from_user.id, photo=kitty_photo, reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)