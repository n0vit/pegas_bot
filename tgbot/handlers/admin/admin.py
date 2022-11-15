from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import InlineKeyboardButton, Message
from aiogram.utils.deep_linking import create_startgroup_link
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ...services.base_repo import BaseHttpRepository
from ..helpers.scheduler import create_task, reg_update

router = Router()


@router.message((F.text == "/start") & (F.chat.type == "private"))
async def command_start_handler(message: Message, bot: Bot) -> None:
    print(message.dict(exclude_none=True))
    link = await create_startgroup_link(bot, payload="add_group")
    markup = InlineKeyboardBuilder()
    markup.add(InlineKeyboardButton(text="Добавить бота", url=link))

    await message.answer(
        f"Привет, <b>{message.from_user.full_name}!</b> \
    \n  Добавь меня в чат|канал для рассылки и дай разрешение отправлять сообщения",
        reply_markup=markup.as_markup(),
    )


@router.message(Command(commands=["add_group"]))
async def command_start_handler(message: Message, command: CommandObject) -> None:
    args = command.args
    reg_update(group=args, chat_id=str(message.chat.id))
    models = BaseHttpRepository().get_schedule(group=args, chat_id=str(message.chat.id))
    create_task(models)
    await message.answer(
        f"Группа {args} \
    \n    Добавлена",
    )
