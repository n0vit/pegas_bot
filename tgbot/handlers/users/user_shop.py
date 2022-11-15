from aiogram.types import CallbackQuery, ChatActions, Message

from ...handlers.helpers.messages_chain import MessagesChain
from ...keyboards.callbacks import callback_shop
from ...keyboards.inline.shop_inline import Shop
from ...loader import prodamus_repo, shop_repo, user_repo
from ...models.prodamus_model import InvoiceModel
from ...states.user_sate import UserState


async def shop_menu(m: Message):
    await ChatActions.typing()
    courses = await shop_repo.get_all_curses()
    user = await user_repo.find_by_id_user(str(m.from_user.id))
    user_level = user.level
    courses = list(_ for _ in courses if _.level <= user_level and _.level != 0)
    text = "Выбери интересующий тебя курс \n"
    await m.answer(text, reply_markup=Shop.shop_menu(courses, callback_shop))


async def about_course(query: CallbackQuery, callback_data: dict):
    await ChatActions.typing()
    id = callback_data["id"]
    course = await shop_repo.get_course(id)
    plans = list(_ for _ in course.plans if _.is_visible)
    markup = Shop.course_plans(plans, callback_shop)
    await MessagesChain.chain_read(
        query.message, description=course.description, markup=markup
    )


async def about_plan(query: CallbackQuery, callback_data: dict):
    await ChatActions.typing()
    id = callback_data["id"]
    uid = str(query.from_user.id)
    user = await user_repo.find_by_id_user(uid)
    plan = await shop_repo.get_course_plan(plan_id=id)
    price = plan.priceRub if user.currency == "rub" else plan.priceUsd
    discount = user.bonusBalance
    if user.bonusBalance > price:
        price = "1"
        discount = "0"
    if user.phone is None:
        return await query.message.answer(
            text="Передайте свой номер, чтобы мы могли выслать вам чек",
            reply_markup=Shop.contactUser(),
        )
    elif user.email is None:
        await UserState.user_email.set()
        return await query.message.answer(
            text="Введи свой email  для привязки аккаунта"
        )

    link = prodamus_repo.create_link(
        InvoiceModel(
            orderId=plan.id,
            customer_extra=uid,
            phone=user.phone,
            email=user.email or " ",
            prQuantity="1",
            prSku=plan.name.replace(" ", "_"),
            currency=user.currency,
            urlReturn=f"https://t.me/Bali_Ceramist_bot?start={user.uid}_{plan.id}_cansel",
            urlSuccess=f"https://t.me/Bali_Ceramist_bot?start=sucsses_{user.uid}_{plan.id}",
            paidContent="Paid_Content",
            taxType="0",
            paymentMethod="1",
            paymentObjectL="1",
            urlNotification=" ",
            discountValue=str(discount),
            prName=plan.name.replace(" ", "_"),
            prPrice=str(price),
        )
    )
    markup = Shop.pay(link)
    await MessagesChain.chain_read(query.message, plan.description, markup)
