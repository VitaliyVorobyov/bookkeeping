from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery


async def delete_mess(call: CallbackQuery, bot: Bot):
    count = 0
    while True:
        try:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - count)
            count += 1
        except TelegramBadRequest:
            break
