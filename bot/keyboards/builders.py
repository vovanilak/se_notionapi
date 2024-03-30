from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardBuilder
from aiogram import types

def reply(lst):
    builder = ReplyKeyboardBuilder()
    for j in lst:
        builder.add(types.KeyboardButton(text=j))
    return builder.adjust(3).as_markup(resize_keyboard=True)