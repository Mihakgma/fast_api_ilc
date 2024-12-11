from typing import Union
from datetime import datetime

from pydantic import BaseModel

from app.classes.id_maker import IdMaker


class Protocol(BaseModel):
    id: int = IdMaker.get_id("Protocol")
    published_date: Union[datetime, None] = None

    def __str__(self):
        return str(self.id)
