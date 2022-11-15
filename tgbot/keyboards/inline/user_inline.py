from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..callbacks import callback_user_controls


class UserInline:
    @staticmethod
    def bind_email(axl_user_id: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(
            InlineKeyboardButton(
                text="Привязать Email",
                callback_data=callback_user_controls.new(
                    action="bind_email", id=axl_user_id
                ),
            )
        )
        return markup
