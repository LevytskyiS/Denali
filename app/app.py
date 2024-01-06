from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.exceptions import TelegramBadRequest
from aiogram.methods import DeleteWebhook
from pytube.exceptions import AgeRestrictedError

from config import config
from app.keyboards import kb
from app.commands import START_MSG, DESC_MSG, HELP_MSG
from memes.meme import get_random_meme
from youtube.yt_downloader import get_youtube_video, remove_downloaded_video

from celery_config.tasks import test_func

bot = Bot(config.API_KEY, parse_mode=ParseMode.HTML)
# bot.set_my_commands(["start"])
dp = Dispatcher()


async def on_startup(_):
    print("The bot is running...")
    # asyncio.create_task(schedule_func())


@dp.message(Command("start"))
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
            await bot.send_message(
                chat_id=message.chat.id, text="Try one more time, the file is damaged."
            )
    else:
        await bot.send_photo(chat_id=message.chat.id, photo=meme)


@dp.message(lambda msg: "youtube.com" in msg.text)
async def download_yt_video(msg: types.Message):
    try:
        video_path = await get_youtube_video(msg.text)
    except AgeRestrictedError as e:
        return await msg.answer(
            text="Video is age restricted, and can't be accessed without logging in to Youtube."
        )

    if video_path:
        await bot.send_video(
            chat_id=msg.from_user.id,
            video=FSInputFile(video_path),
            width=1280,
            height=720,
        )
        await remove_downloaded_video(video_path)
    else:
        await msg.answer(text="The file size is grater than 50 MB")


@dp.message(Command("celery"))
async def command_celery_handler(message: Message) -> None:
    result = test_func.delay()
    await message.answer(text="Celery works")


async def main() -> None:
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)
    await bot.set_my_commands(["start"])
