from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from core.keyboards.inline import main_menu_kb
from core.utils.callbackdata import Back
from core.utils.dbconnect import Request


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, request: Request, state: FSMContext):
    await state.clear()
    await request.add_user(message.from_user.id, message.from_user.first_name)
    await message.answer(f'Выберите категорию:',
                         reply_markup=main_menu_kb())


@router.callback_query(Back.filter(F.name_button == "back"))
async def cmd_back(call: CallbackQuery, bot: Bot, state: FSMContext, request: Request):
    await state.clear()
    await update_message(call, bot, request)


async def update_message(call: CallbackQuery, bot: Bot, request: Request):
    res = await request.stat(call.from_user.id, 1)
    result = ""
    for key in res:
        result += f'{key[0]} - {key[1]}\n'
    await bot.edit_message_text(f'На данный момент на ваших счетах:\n\n{result}',
                                call.from_user.id, call.message.message_id,
                                reply_markup=main_menu_kb())