from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.exceptions import TelegramBadRequest
from aiogram.methods import DeleteWebhook
from instagrapi.exceptions import PleaseWaitFewMinutes

# from aiogram.utils.exceptions import WrongFileIdentifier, InvalidHTTPUrlContent

from config import config
from app.keyboards import kb
from app.commands import START_MSG, DESC_MSG, HELP_MSG
from memes.meme import get_random_meme
from youtube.yt_downloader import get_youtube_video, remove_downloaded_video
from instagram.inst import get_media

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


@dp.message(lambda msg: "youtube.com" in msg.text)
async def download_yt_video(msg: types.Message):
    video_path = await get_youtube_video(msg.text)

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


@dp.message(lambda msg: "https://www.instagram.com" in msg.text)
async def download_instagram_content(msg: Message):
    try:
        photos = await get_media(msg.text)
    except PleaseWaitFewMinutes as e:
        return await msg.answer(e.message)

    if photos:
        for photo in photos:
            try:
                await bot.send_document(chat_id=msg.from_user.id, document=str(photo))
            # except WrongFileIdentifier as e:
            #     await msg.answer(
            #         f"This video is pretty big. Use this link below to download it:\n {photo}."
            #     )
            # except InvalidHTTPUrlContent as e:
            #     await msg.answer(
            #         "It seems that this link has some issues.\nTry again or get another link."
            #     )
            except Exception as e:
                await msg.answer(str(e))


async def main() -> None:
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)
    await bot.set_my_commands(["start"])
