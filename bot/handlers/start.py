from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from bot.keyboards import builders, inline
from aiogram.fsm.context import FSMContext
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
import traceback
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import URLInputFile, FSInputFile
from main import MainProcess
from server.uguu import post_uguu
from person.test import Test
import os

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text='Привет👋 Это бот для добавления данных о Легионерах и Штатных Сотрудниках из Google Sheets в Notion🚀'
    )
    await message.answer(
        text='Используй /menu, чтобы выбрать, кого добавить'
    )

@router.message(Command('menu'))
async def cmd_menu(message: Message):
    await message.answer(
        text='Выбери участника⬇️',
        reply_markup=builders.reply(
            ('Легионер', 'Штатный Сотрудник')
        )
    )

@router.message(F.text.in_((
    ('Легионер', 'Штатный Сотрудник')
)))
async def who(message: Message, state: FSMContext):
    await state.update_data(who=message.text)
    await message.answer(
        text='Пожалуйста, введи номер строки из Google Sheets',
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(F.text == "Связаться с разработчиком")
async def developer(message: Message):
    await message.answer(
        text='Контакт разработчика',
        reply_markup=inline.url(
                        text='Чат📨', 
                        url='https://t.me/vovanilak'
                    )
    )

@router.message(F.text.isdigit())
async def layer2(message: Message, state: FSMContext):
    await state.update_data(row=int(message.text))
    await message.answer(
        text='Выбери действие⬇️',
        reply_markup=builders.reply(
            (('Публикация', 'Графики', 'Результаты')) # Получить графики
        )
    )

@router.message(F.text.in_(('Публикация', 'Графики', 'Результаты'))) # получить графики
async def post_notion(message: Message, state: FSMContext):

    a = await state.get_data()
    await message.answer(
        text='Подожди немного... Я напишу, когда будет готово!',
        reply_markup=ReplyKeyboardRemove()
    )
    try:
        mp = MainProcess(a['who'], a['row'])
        if message.text == 'Результаты':

            txt = mp.do_pretty()
            await message.answer(
                text=txt
            )
        
        if message.text == 'Публикация':
            await message.answer('Подожди ещё, пожалуйста, публикую карточку в notion')
            res = mp.run()

            await message.answer(
                text=f'Готово! Можешь проверить карточку',
                reply_markup=inline.url(
                    text='Ссылка🔗',
                    url=res['url']
                )
            )

        if message.text == 'Графики':
            png_files = mp.get_tmp_imgs()
            album_builder = MediaGroupBuilder()
            for filename in png_files:   
                album_builder.add_photo(media=URLInputFile(filename))
            await message.answer_media_group(media=album_builder.build())

    except Exception as err:
        await message.answer(
            text=f'Ошибочка...\n{traceback.format_exc()[:4000]}'
        )

    await cmd_menu(message)
    
@router.message()
async def error(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Что-то пошло не так... Перевожу на главное меню'
    )
    await cmd_menu(message)

