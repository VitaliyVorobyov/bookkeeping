from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from core.utils.settings import settings
from core.utils.dbconnect import Request
from core.keyboards.inline import subcategory_statistic_kb, back_kb
from core.utils.callbackdata import MainMenu, SubcategoryStat
from core.utils.states import StatisticsState


router = Router()


@router.callback_query(MainMenu.filter(F.name_button == "statistic"))
async def cmd_send_date(call: CallbackQuery, bot: Bot, state: FSMContext, request: Request):
    category = 1
    sub_category = await request.select_sub_category(settings.bots.user_id_1, category)
    await state.set_state(StatisticsState.sub_category)
    await bot.edit_message_text('Выберите одну или несколько категорий:\n'
                                '**по умолчанию выведутся все категории**',
                                call.from_user.id, call.message.message_id,
                                reply_markup=subcategory_statistic_kb(sub_category))


@router.callback_query(SubcategoryStat.filter(F.add_name_button == "subcategory"), StatisticsState.sub_category)
async def cmd_select_sub_category(call: CallbackQuery, callback_data: SubcategoryStat, bot: Bot,
                                  state: FSMContext, request: Request):
    context = await state.get_data()
    category = 1
    get_sub_category = context.get('sub_category')
    sub_category = await request.select_sub_category(settings.bots.user_id_1, category)

    if get_sub_category is None:
        get_sub_category = {str(callback_data.id_sub_category): callback_data.name_button+'🟢'}
        await state.update_data(sub_category=get_sub_category)
    elif str(callback_data.id_sub_category) in get_sub_category:
        get_sub_category.pop(str(callback_data.id_sub_category))
        await state.update_data(sub_category=get_sub_category)
    else:
        get_sub_category.update({str(callback_data.id_sub_category): callback_data.name_button+'🟢'})
        await state.update_data(sub_category=get_sub_category)

    sub_category.update({int(key): value for key, value in get_sub_category.items()})
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                                        reply_markup=subcategory_statistic_kb(sub_category))


@router.callback_query(SubcategoryStat.filter(F.add_name_button == "send"))
async def cmd_send_data(call: CallbackQuery, bot: Bot, request: Request, state: FSMContext):
    context = await state.get_data()
    sub_category = context.get('sub_category')
    if sub_category is None or len(sub_category) == 0:
        sub_category_list = list((await request.select_sub_category(settings.bots.user_id_1, 1)).keys())
    else:
        sub_category_list = list({int(key): value for key, value in sub_category.items()}.keys())
    res = await request.stat_all(settings.bots.user_id_1, 1, sub_category_list)
    result = ""
    for key in res:
        result += f'{key[0]} - {key[1]}₽ - {key[2]}\n'
    await bot.edit_message_text(f'Ваши взносы:\n\n{result}', call.from_user.id, call.message.message_id,
                                reply_markup=back_kb())
