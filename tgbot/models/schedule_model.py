from datetime import datetime
from typing import List

from pydantic import BaseModel


class Room(BaseModel):
    name: str
    area: str
    address: str


class Teacher(BaseModel):
    name: str
    dep: str | None
    subdep: str | None
    pos: str | None


class ScheduleModel(BaseModel):
    chat_id: str
    group: str
    pairnumber: int
    timestart: datetime
    timeend: datetime
    edworkkind: str
    subgroup: str | None = None
    room: Room | None = None
    dis: str | None = None
    online: bool = False
    withdist: bool = True
    teacher: Teacher | None = None
    links: List[dict] | None
