from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from core.utils.dbconnect import Request
from core.keyboards.inline import back_kb, select_sub_category_kb, numbers_kb
from core.utils.callbackdata import MainMenu, SelectSubCategory, NewSubCategory, Numbers, Send
from core.utils.states import AddDataState
from core.handlers.basic import update_message


router = Router()


@router.callback_query(MainMenu.filter(F.name_button == "input"))
async def cmd_amount(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(AddDataState.category)
    await state.update_data(category=1)
    await state.set_state(AddDataState.amount)
    await bot.edit_message_text('Введите сумму:', call.from_user.id, call.message.message_id,
                                reply_markup=numbers_kb())


@router.callback_query(Numbers.filter(), AddDataState.amount)
async def cmd_numbers(call: CallbackQuery, callback_data: Numbers, bot: Bot, state: FSMContext):
    context = await state.get_data()
    amount = context.get('amount')
    if amount is not None and callback_data.name_button == '◀️':
        amount = amount[:-1]
    elif callback_data.name_button != '◀️':
        amount = (str(amount)+callback_data.name_button).replace('None', '')
    await state.update_data(amount=f'{amount}')
    await state.set_state(AddDataState.amount)
    await bot.edit_message_text(f'Внесено: {amount} ₽', call.from_user.id, call.message.message_id,
                                reply_markup=numbers_kb())


@router.callback_query(Send.filter(), AddDataState.amount)
async def cmd_select_sub_category(call: CallbackQuery, bot: Bot, state: FSMContext, request: Request):
    await state.set_state(AddDataState.sub_category)
    category = 1
    sub_category = await request.select_sub_category(133233628, category)
    if len(sub_category) == 0:
        await state.set_state(AddDataState.new_sub_category)
        await bot.edit_message_text('Вы еще не добавили ни одной категории. Введите название новой категории:',
                                    call.from_user.id, call.message.message_id, reply_markup=back_kb())
    else:
        await state.set_state(AddDataState.sub_category)
        await bot.edit_message_text('Выберите подкатегорию:', call.from_user.id, call.message.message_id,
                                    reply_markup=select_sub_category_kb(sub_category))


@router.message(AddDataState.new_sub_category)
async def cmd_new_sub_category(message: Message, bot: Bot, state: FSMContext, request: Request):
    await state.update_data(new_sub_category=message.text)
    category = 1
    name_sub_category = message.text
    await request.add_sub_category(133233628, category, name_sub_category)
    sub_category = await request.select_sub_category(133233628, category)
    await state.set_state(AddDataState.sub_category)
    await bot.delete_message(message.from_user.id, message.message_id)
    for i in range(100):
        try:
            await bot.edit_message_text('Категория добавлена! Выберите подкатегорию:',
                                        message.from_user.id, message.message_id-i,
                                        reply_markup=select_sub_category_kb(sub_category))
            break
        except TelegramBadRequest:
            pass
        if i == 99:
            await bot.send_message(message.from_user.id, 'Категория добавлена! Выберите подкатегорию:',
                                   reply_markup=select_sub_category_kb(sub_category))


@router.callback_query(SelectSubCategory.filter(), AddDataState.sub_category)
async def save_data_in_db(call: CallbackQuery, bot: Bot, callback_data: SelectSubCategory, state: FSMContext,
                          request: Request):
    context = await state.get_data()
    amount = int(context.get('amount'))
    category_id = 1
    sub_category = callback_data.id_sub_category
    await request.add_entry(133233628, category_id, sub_category, amount)
    await state.clear()
    await update_message(call, bot, request)


@router.callback_query(NewSubCategory.filter(F.name_button == "new category"))
async def new_category(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(AddDataState.new_sub_category)
    await bot.edit_message_text('Введите название новой категории:', call.from_user.id, call.message.message_id,
                                reply_markup=back_kb())
