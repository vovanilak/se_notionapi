from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from bot.keyboards import builders, inline
from aiogram.fsm.context import FSMContext
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
import traceback

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
        text='Выбери действие⬇️',
        reply_markup=builders.reply(
            ('Легионер', 'Штатный Сотрудник', "Связаться с разработчиком")
        )
    )

@router.message(F.text.in_(('Легионер', 'Штатный Сотрудник')))
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
async def post_notion(message: Message, state: FSMContext):
    from main import Anketa

    a = await state.get_data()
    await message.answer(
        text='Подожди немного... Я напишу, когда будет готово!'
    )
    try:
        if a['who'] == 'Штатный Сотрудник':

            person = Anketa(url=Anketa.URL_STAFF,
                            row=int(message.text),
                            json_file='data/staff.json',
                            start_result_column=11)
            await message.answer(
                text=f'Имя сотрудника: {person.name}'
            )
            
            res = person.post_staff()
        elif a['who'] == 'Легионер':

            person = Anketa(url=Anketa.URL_LIGA,
                            row=int(message.text),
                            json_file='data/short2_back.json',
                            start_result_column=13)
            await message.answer(
                text=f'ID легионера: {person.id}'
            )
            
            res = person.post_liga()
        else:
            await cmd_menu(message)

        await message.answer(
            text='Готово! Можешь проверить карточку',
            reply_markup=inline.url(
                text='Ссылка🔗',
                url=res['url']
            )
        )
    except Exception as err:
        #await message.answer(str(err))
        await message.answer(
            text=f'Ошибочка...\n{traceback.format_exc()[:4000]}\nОна может возникнуть в случае, когда указана несуществующая строка. Могут быть иные причины. Попробуйте ещё раз, либо свяжитесь с разработчиком'
        )
        #await cmd_menu(message)

    await cmd_menu(message)
    
@router.message()
async def error(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Что-то пошло не так... Перевожу на главное меню'
    )
    await cmd_menu(message)



