from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton


b1 = KeyboardButton(text="/start")
b2 = KeyboardButton(text="/help")
b3 = KeyboardButton(text="/desc")
b4 = KeyboardButton(text="/meme")
b5 = KeyboardButton(text="/celery")
kb = ReplyKeyboardMarkup(keyboard=[[b1, b2, b3, b4, b5]], resize_keyboard=True)
