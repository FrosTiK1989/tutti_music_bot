import logging
import os

import requests
from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
EXCEPT = ["Главная", "Ноты", "", "Музыканты"]
URL = "https://pianokafe.com/search/?q="

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="start")
async def start_massage(message: types.Message):
    await message.answer(
        "Привет! Я бот, который помогает найти тебе ноты\n"
        "для твоих любимых музыкальных композиций!\n"
        "Для того чтобы начать поиск, просто напиши мне\n"
        "Название исполнителя или композицию"
    )


@dp.message_handler(content_types=["text"])
async def answer_for_request(message: types.Message):
    search = message.text.replace(" ", "+")
    req = requests.get(URL + search)
    soup = BeautifulSoup(req.text, "lxml")
    note = (
        soup.find(class_="search-page")
        .find(class_="search-result")
        .find_all("a")
    )
    all_songs = []
    for item in note:
        item_text = item.text
        clear_text = item_text.lstrip("Ноты ")
        item_url = "https://pianokafe.com" + item.get("href")
        if item_text not in EXCEPT:
            all_songs.append([clear_text, item_url])
    return await bot.send_message(message.chat.id, f"{str(all_songs[:6])}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
