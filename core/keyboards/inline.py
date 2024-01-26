from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.utils.callbackdata import (MainMenu, Back, SelectSubCategory, NewSubCategory,
                                     Numbers, Send, SelectCategoryStat, SubcategoryStat)


def main_menu_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='Внести ✏️', callback_data=MainMenu(name_button='input'))
    kb.button(text='Статистика 📊', callback_data=MainMenu(name_button='statistic'))
    kb.adjust(2)
    return kb.as_markup()


def back_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='Назад ⬅️', callback_data=Back(name_button='back'))
    kb.adjust(1)
    return kb.as_markup()


def select_sub_category_kb(sub_category: dict):
    kb = InlineKeyboardBuilder()
    for key, value in sub_category.items():
        kb.button(text=value, callback_data=SelectSubCategory(id_sub_category=key, name_button=value))
    kb.button(text='Новая категорию 🆕', callback_data=NewSubCategory(name_button='new category'))
    kb.button(text='Назад ⬅️', callback_data=Back(name_button='back'))
    kb.adjust(1)
    return kb.as_markup()


def numbers_kb():
    kb = InlineKeyboardBuilder()
    list_kb = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '◀️'
    ]
    for i in list_kb:
        kb.button(text=i, callback_data=Numbers(name_button=i))
    kb.button(text='Готово ✅', callback_data=Send(name_button='send'))
    kb.button(text='Назад ⬅️', callback_data=Back(name_button='back'))
    kb.adjust(3, 3, 3, 2, 1, 1)
    return kb.as_markup()


def statistics_kb(keyboard: dict):
    kb = InlineKeyboardBuilder()
    for key, value in keyboard.items():
        kb.button(text=value, callback_data=SelectCategoryStat(id_category=key, name_button=value))
    kb.button(text='Далее ➡️', callback_data=SelectCategoryStat(id_category=0, name_button='send'))
    kb.button(text='Назад ⬅️', callback_data=Back(name_button='back'))
    kb.adjust(2, 1, 1)
    return kb.as_markup()


def subcategory_statistic_kb(sub_category: dict):
    kb = InlineKeyboardBuilder()
    for key, value in sub_category.items():
        kb.button(text=value, callback_data=SubcategoryStat(id_sub_category=key, name_button=value,
                                                            add_name_button='subcategory'))
    kb.button(text='Готово ✅', callback_data=SubcategoryStat(id_sub_category=0, name_button='send',
                                                             add_name_button='send'))
    kb.button(text='Назад ⬅️', callback_data=Back(name_button='back'))
    kb.adjust(1)
    return kb.as_markup()
