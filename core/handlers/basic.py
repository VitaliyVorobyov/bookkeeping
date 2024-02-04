from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from core.utils.settings import settings
from core.keyboards.inline import main_menu_kb
from core.utils.callbackdata import Back
from core.utils.dbconnect import Request


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, request: Request, state: FSMContext):
    await state.clear()
    await request.add_user(message.from_user.id, message.from_user.first_name)
    await message.answer_photo(
        'https://vsegda-pomnim.com/uploads/posts/2022-03/1648753820_2-vsegda-pomnim-com-p-ozero-baikal-zima-foto-2.jpg',
        f'Выберите категорию:',
        reply_markup=main_menu_kb())


@router.callback_query(Back.filter(F.name_button == "back"))
async def cmd_back(call: CallbackQuery, bot: Bot, state: FSMContext, request: Request):
    await state.clear()
    try:
        await update_message(call, bot, request)
    except TelegramBadRequest:
        await call.message.answer_photo(
            'https://vsegda-pomnim.com/uploads/posts/2022-03/1648753820_2-'
            'vsegda-pomnim-com-p-ozero-baikal-zima-foto-2.jpg',
            f'Выберите категорию:',
            reply_markup=main_menu_kb())


async def update_message(call: CallbackQuery, bot: Bot, request: Request):
    res = await request.stat(settings.bots.user_id_1, 1)
    result = ""
    for key in res:
        result += f'{key[0]} - {key[1]}\n'
    await bot.edit_message_caption(call.from_user.id, call.message.message_id,
                                   caption=f'Состояние ваших взносов на текущую дату:\n\n{result}',
                                   reply_markup=main_menu_kb())
