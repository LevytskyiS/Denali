import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.methods.send_animation import SendAnimation
from aiogram.types.input_file import InputFile, URLInputFile
from aiogram.exceptions import TelegramBadRequest
from aiogram.methods import DeleteWebhook

from config import config
from app.keyboards import kb
from memes.meme import get_random_meme
from app.commands import START_MSG, DESC_MSG, HELP_MSG

bot = Bot(config.API_KEY, parse_mode=ParseMode.HTML)
dp = Dispatcher()


async def on_startup(_):
    print("The bot is running...")
    # asyncio.create_task(schedule_func())


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(START_MSG)


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer(text=HELP_MSG, reply_markup=kb)


@dp.message(Command("desc"))
async def command_help_handler(message: Message) -> None:
    await message.answer(text=DESC_MSG)


@dp.message(Command("meme"))
async def command_meme_handler(message: Message) -> None:
    meme = await get_random_meme()
    if meme.endswith(".gif"):
        try:
            await bot.send_document(chat_id=message.chat.id, document=meme)
        except TelegramBadRequest as e:
            await message.answer(text="Try one more time, the file is damaged.")
    else:
        await bot.send_photo(chat_id=message.chat.id, photo=meme)


@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)
