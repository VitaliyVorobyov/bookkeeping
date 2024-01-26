from aiogram.filters.callback_data import CallbackData


class MainMenu(CallbackData, prefix='main'):
    name_button: str


class SelectCategory(CallbackData, prefix='category'):
    id_category: int
    name_button: str


class Back(CallbackData, prefix='back'):
    name_button: str


class Send(CallbackData, prefix='send'):
    name_button: str


class Numbers(CallbackData, prefix='numbers'):
    name_button: str


class SelectSubCategory(CallbackData, prefix='subcategory'):
    id_sub_category: int
    name_button: str


class SelectCategoryStat(CallbackData, prefix='subcategory'):
    id_category: int
    name_button: str


class NewSubCategory(CallbackData, prefix='newsubcategory'):
    name_button: str


class Statistic(CallbackData, prefix='statistic'):
    name_button: str


class SeleclPeriod(CallbackData, prefix='period'):
    name_button: str


class DayMountYear(CallbackData, prefix='period'):
    name_button: str
    add_name_button: str


class Day(CallbackData, prefix='day'):
    name_button: int


class Month(CallbackData, prefix='month'):
    id_month: int
    name_button: str


class Year(CallbackData, prefix='year'):
    name_button: int


class SubcategoryStat(CallbackData, prefix='subcategory'):
    id_sub_category: int
    name_button: str
    add_name_button: str
