from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class UserButtons:
    @staticmethod
    def menu() -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [
            KeyboardButton(text="Профиль"),
            KeyboardButton(text="Курсы"),
            KeyboardButton(text="Бонусы"),
        ]
        markup.add(*buttons)
        return markup
