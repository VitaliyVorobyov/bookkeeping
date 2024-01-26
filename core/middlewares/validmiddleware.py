from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class ValidationMiddleware(BaseMiddleware):
    def __init__(self, users: list[int]):
        super().__init__()
        self.users = users

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data["event_from_user"]
        if user.id not in self.users:
            await event.answer("Вы не авторизованы для использования этого бота.")
        else:
            data['users'] = self.users
            return await handler(event, data)
