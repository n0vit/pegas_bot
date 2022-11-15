from aiogram import Bot, F, Router
from aiogram.filters.chat_member_updated import (
    ADMINISTRATOR,
    IS_NOT_MEMBER,
    ChatMemberUpdatedFilter,
)
from aiogram.types import ChatMemberUpdated

router_group = Router()
router_group.my_chat_member.filter(F.chat.type.in_({"group", "supergroup", "channel"}))


@router_group.my_chat_member(
    (ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> ADMINISTRATOR))
)
async def bot_added_as_admin(event: ChatMemberUpdated, bot: Bot):
    # Самый простой случай: бот добавлен как админ.
    # Легко можем отправить сообщение
    await bot.send_message(
        chat_id=event.chat.id,
        text=f"Привет! Спасибо, что добавили меня в "
        f'"{event.chat.title}"'
        f"Как администратора  чата",
    )
