import logging

import coloredlogs
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .config import load_config
from .models.schedule_model import ScheduleModel

coloredlogs.install(logging.DEBUG)

logger = logging.Logger(__name__, level=logging.DEBUG)
config = load_config("bot.ini")
schedule_model = ScheduleModel

jobstores = {"default": SQLAlchemyJobStore(url="sqlite:///jobs.sqlite")}
scheduler = AsyncIOScheduler(jobstores=jobstores)
