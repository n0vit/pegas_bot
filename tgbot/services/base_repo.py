import datetime
from typing import Any, List

import requests

from ..models.schedule_model import ScheduleModel


class BaseHttpRepository:
    def _dateparser(self, *args, **kwargs) -> dict[str, Any]:
        timestart = kwargs.get("timestart", 0)
        kwargs["timestart"] = datetime.datetime.fromtimestamp(timestart)
        timeend = kwargs.get("timeend", 0)
        kwargs["timeend"] = datetime.datetime.fromtimestamp(timeend)
        kwargs["chat_id"] = args[0]
        kwargs["group"] = args[1]
        return kwargs

    def get_schedule(self, group: str, chat_id: str) -> List[ScheduleModel]:
        now = datetime.date.today().isoformat()
        after = datetime.date.today() + datetime.timedelta(days=2)

        response = requests.get(
            f"https://beluni.ru/schedule/g/{group}?from={now}&to={after}&qdist=1"
        )
        data = [self._dateparser(chat_id, group, **_) for _ in response.json()]
        data = [ScheduleModel.parse_obj(_) for _ in data]
        return data
