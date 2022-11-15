from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.deep_linking import get_start_link
from pydantic import validate_email

from ...keyboards.buttons.user_buttons import UserButtons
from ...keyboards.inline.user_inline import UserInline
from ...loader import axl_repo, user_model, user_repo
from ...models.axl_models import AxlSearchUser, AxlUserModel
from ...states.user_sate import UserState


async def user_start(m: Message, state: FSMContext) -> Message:
    if state:
        await state.finish()
    refer = m.get_args()
    id = str(m.from_user.id)
    check_user = await user_repo.find_by_id_user(id)
    lang = m.from_user.language_code
    if refer.startswith("axl_"):
        axl_id = refer[4:]
        emails = await axl_repo.find_user(AxlSearchUser(id=axl_id, fields="{email}"))
        em = emails[0]["email"]
        await user_repo.update_user(
            id=id,
            new_data={"email": em, "axl_id": axl_id},
        )
        await m.delete()
        return await m.answer(
            text=f"Email <b>{em}</b> успешно привязан к вашему аккаунту"
        )

    if lang == "ru":
        currency = "rub"
    else:
        currency = "usd"

    if check_user is None:
        await user_repo.add_user(
            user_model.UserModel(
                uid=id,
                firstName=m.from_user.first_name,
                lastName=m.from_user.last_name,
                userName=m.from_user.username,
                lang=lang,
                currency=currency,
                refer=refer,
                referals=[],
                bonusBalance=0,
                fiatBalance=0,
                level=0,
            )
        )

        check_refer = await user_repo.find_by_id_user(refer)
        if check_refer and id != refer:
            if id not in check_refer.referrals:
                await m.bot.send_message(
                    refer,
                    text=f"Поздравляем ! пользователь <a href='tg://user?self={id}'>{m.from_user.first_name}</a>, перешел по твоей реф ссылке\
                    \n  ты получаешь 500 бонусных баллов!",
                )
                await m.bot.send_message(
                    918565441,
                    text=f"Зарегистрирован пользователь {m.from_user.first_name}\
                    \n рефер <a href='tg://user?self={refer}'>{check_refer.firstName}</a>",
                )
                referrals = check_refer.referrals
                referrals.append(id)
                balance = check_refer.bonusBalance + 500
                user_repo.upsert(
                    refer, {"referrals": referrals, "bonusBalance": balance}
                )
        else:
            await m.bot.send_message(
                918565441,
                text=f"Зарегистрирован пользователь <a href='tg://user?self={id}'>{m.from_user.first_name}</a>",
            )
    await m.reply(f"Hello, user! {refer or '!'}", reply_markup=UserButtons.menu())


async def getRefLink(m: Message) -> None:
    id = m.from_user.id
    link = await get_start_link(payload=id)
    await m.answer(
        f"Вот твоя персональная ссылка!\
        \n {link} \
        \n  приводи друзей и получай бонусы!!!"
    )


async def saveContact(message: Message) -> None:
    contact = message.contact
    await user_repo.update_user(
        str(message.from_user.id), new_data={"phone": str(contact.phone_number)}
    )

    user = await user_repo.find_by_id_user(str(message.from_user.id))
    if user.email is None:
        await message.answer(text="Отлично! Твой номер получен!")
        await message.answer(text="Введи свой email  для привязки аккаунта")
        await UserState.user_email.set()
    else:
        await message.answer(
            text="Отлично! Мы получили твои данные, теперь ты можешь перейти к оплате"
        )


async def bindEmail(
    query: CallbackQuery, state: FSMContext, callback_data: dict
) -> None:
    id = callback_data["self"]
    await axl_repo.add_che_email_tag(id)
    await state.finish()
    await query.message.edit_text(
        "На вашу почту отправлено письмо с ссылкой для подтверждения привязки \
        \n  после перехода по ссылке <b>обязательно нажмите START  </b>, иначе привязка не выполнится"
    )


async def saveEmail(message: Message, state: FSMContext) -> Message | None:
    user = await user_repo.find_by_id_user(str(message.from_user.id))
    try:
        email = validate_email(message.text)

        axl_check_email = await axl_repo.find_user(
            AxlSearchUser(email=email[1], fields="{id,firstName}")
        )
        if axl_check_email:
            axl_emails = axl_check_email[0]
            return await message.answer(
                text=f"Данный email <b>{email[1]}</b> уже используются с именем\
                \n<b>{axl_emails['firstName']}</b> \
                \n Если данная почта принадлежит вам, нажмите, привязать почту \
                \n Или же введите другой email",
                reply_markup=UserInline.bind_email(axl_emails["id"]),
            )

        axl_user_id = await axl_repo.create_user(
            AxlUserModel(
                email=email[1],
                firstName=user.firstName,
                gender="0",
                phone=user.phone,
                middleName=user.lastName,
                groups=[],
                tags=["FromTgBot"],
            )
        )

    except Exception as e:
        print(e)
        return await message.answer(
            text="Введи email еще раз, возможно ты совершил опечатку"
        )

    await user_repo.update_user(
        str(message.from_user.id), new_data={"email": email[1], "axl_id": axl_user_id}
    )
    await state.finish()
    if user.phone is None:
        await message.answer(text="Отлично! Email получен!")
        await message.answer(
            text="Введи свой номер   для дополнительной привязки аккаунта"
        )

    else:
        await message.answer(
            text="Отлично! Мы получили твои данные, теперь ты можешь перейти к оплате"
        )


async def zero_course(m: Message) -> None:
    await m.answer("начало курса..")
