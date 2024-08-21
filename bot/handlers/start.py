from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from bot.keyboards import builders, inline
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
import traceback
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import URLInputFile, FSInputFile
from main import MainProcess
from server.uguu import post_uguu
from person.test import Test
from bot.handlers.states import Card
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
async def cmd_menu(message: Message, state: FSMContext):
    await state.set_state(Card.who)
    await message.answer(
        text='Выбери участника⬇️',
        reply_markup=builders.reply(
            ('Легионер', 'Штатный Сотрудник')
        )
    )

@router.message(
    StateFilter(Card.who),
    F.text.in_((
        ('Легионер', 'Штатный Сотрудник')
    ))
)
async def who(message: Message, state: FSMContext):
    await state.set_state(Card.row_as_test)
    await state.update_data(who=message.text)
    await message.answer(
        text='Пожалуйста, введи номер строки из таблицы АС👇',
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(
    StateFilter(Card.row_as_test),
    F.text.isdigit()
)
async def layer2(message: Message, state: FSMContext):
    await state.set_state(Card.row_vt_test)
    await state.update_data(row_as=int(message.text))
    await message.answer(
        text='Пожалуйста, введи номер строки из таблицы ВТ👇\nИли отправте 0 (ноль) если все ответы должны быть равны 1'
    )
    

@router.message(
    StateFilter(Card.row_vt_test),
    F.text.isdigit()
)
async def layer3(message: Message, state: FSMContext):
    await state.set_state(Card.action)
    await state.update_data(row_vt=int(message.text))
    await message.answer(
        text='Выбери действие⬇️',
        reply_markup=builders.reply(
            (('Публикация', 'Графики', 'Результаты')) # Получить графики
        )
    )

@router.message(
    StateFilter(Card.action),
    F.text.in_(('Публикация', 'Графики', 'Результаты'))
) 
async def post_notion(message: Message, state: FSMContext):
    a = await state.get_data()
    await state.clear()
    await state.set_state(default_state)
    await message.answer(
        text='Подожди немного... Я напишу, когда будет готово!',
        reply_markup=ReplyKeyboardRemove()
    )
    try:
        mp = MainProcess(a['who'], a['row_as'], a['row_vt'])
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

    await cmd_menu(message, state)
    
@router.message(~StateFilter(default_state))
async def error(message: Message, state: FSMContext):
    await state.set_state(default_state)
    await state.clear()
    await message.answer(
        text='Что-то пошло не так... Перевожу на главное меню'
    )
    await cmd_menu(message, state)

@router.message()
async def error(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Что-то пошло не так... Перевожу на главное меню'
    )
    await cmd_menu(message, state)

