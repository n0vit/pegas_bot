import datetime
from typing import List

from aiogram.methods.send_message import SendMessage
from aiogram.types import InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger

from ...loader import logger, scheduler
from ...models.schedule_model import ScheduleModel
from ...services.base_repo import BaseHttpRepository


def reg_update(chat_id: str, group: str) -> None:
    trigger = CronTrigger(hour=5)

    try:
        scheduler.remove_job(chat_id)
    except Exception as e:
        print(e)
    jobs = scheduler.get_jobs()
    for job in jobs:
        if group in job.id:
            scheduler.remove_job(job.id)

    models = BaseHttpRepository().get_schedule(chat_id=chat_id, group=group)
    scheduler.add_job(create_task, trigger, id=chat_id, args=(models,))


def create_task(models: List[ScheduleModel]) -> None:
    """
        Use to schedule
    Args:
        model:  (PydanticModel)
    """

    for model in models:
        date = model.timestart - datetime.timedelta(minutes=5)
        trigger = DateTrigger(
            run_date=date, timezone=datetime.timezone(datetime.timedelta(hours=3))
        )
        id = model.group + model.timestart.isoformat()
        try:
            scheduler.remove_job(id)
        except Exception as e:
            print(e)
        model = models[0]
        scheduler.add_job(anouncer, trigger, name=id, id=id, args=(model,))


async def anouncer(model: ScheduleModel) -> None:
    """
        Anouncer function, don't use manually
    Args:
        model:  (PydanticModel)
    """
    chat_id = model.chat_id
    if model.room:
        room = f"🌏 {model.room.address}\
            \n <u>🏫 {model.room.area}\
            \n 🚪 {model.room.name} </u>"
    else:
        room = ""

    if model.teacher:
        teacher = f"👤 <b>{model.teacher.name}</b>\
            \n {model.teacher.dep} \
            \n {model.teacher.subdep} \
            \n {model.teacher.pos}"
    else:
        teacher = ""
    text = f"""
        Пара: <b>{model.pairnumber}</b>\
        \nГруппа: <b>{model.group}</b>\
        \n<code>{model.dis or ""}</code>\
        \n<i>{model.edworkkind}</i>\
        \n{'online 💻' if model.online else room}\
        \n{teacher}\
        \n <b>{model.timestart.isoformat(sep=' ')}</b>\
        \n <b>{model.timeend.isoformat(sep=' ')}</b>"""

    if model.links:
        markup = InlineKeyboardBuilder()
        markup.add(
            InlineKeyboardButton(
                text=model.links[0]["name"], url=model.links[0]["href"]
            )
        )
    else:
        markup = None
    await SendMessage(chat_id=chat_id, text=text, reply_markup=markup.as_markup())
