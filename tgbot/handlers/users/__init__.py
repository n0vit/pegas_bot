from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import ContentType

from ...keyboards.callbacks import callback_shop, callback_user_controls
from ...states import UserState
from .user import bindEmail, getRefLink, saveContact, saveEmail, user_start
from .user_shop import about_course, about_plan, shop_menu


def usersSetup(dp: Dispatcher) -> None:

    dp.register_message_handler(getRefLink, Text(equals="Бонусы"))
    dp.register_message_handler(user_start, CommandStart(), state="*")
    dp.register_message_handler(shop_menu, commands=["shop"], state="*")
    dp.register_callback_query_handler(
        about_course, callback_shop.filter(action="course")
    )
    dp.register_callback_query_handler(about_plan, callback_shop.filter(action="plan"))
    dp.register_callback_query_handler(
        bindEmail,
        callback_user_controls.filter(action="bind_email"),
        state=UserState.user_email,
    )
    dp.register_message_handler(saveContact, content_types=ContentType.CONTACT)
    dp.register_message_handler(saveEmail, state=UserState.user_email)
