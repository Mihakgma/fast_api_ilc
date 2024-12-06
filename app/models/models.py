from datetime import datetime, date
from typing import List, Union

from pydantic import BaseModel, field_validator, computed_field

from app.classes.id_maker import IdMaker
from app.funct.refine_phone_number import refine_phone_number


class User(BaseModel):

    id: int = IdMaker.get_id('User')
    first_name: str = "Иван"
    surname: str = "Иванович"
    last_name: str = "Иванов"
    birth_date: Union[datetime, None] = None
    email: str = "ivan_ivanch@sibir.ru"
    password: str = "1234"
    phone: str = "0123456789"
    department: str = ""
    roles: List[int] = [1, 2, 3]
    info: str = "some information"

    @computed_field
    @property
    def is_adult(self) -> bool:
        today = date.today()
        if self.birth_date is not None:
            print("is adult property worked")
            return (today - self.birth_date.date()).days >= (18 * 365.25)

    @field_validator("first_name")
    @classmethod
    def check_first_name_length(cls, v) -> str:
        max_length = 30
        if len(v) > max_length:
            raise ValueError(f"First name must be at most <{max_length}> characters.")
        return v

    @field_validator("phone")
    @classmethod
    def check_phone(cls, v: str) -> str:
        max_length = 12
        v = refine_phone_number(v)
        if len(v) > max_length:
            raise ValueError(f"Phone number must be at most <{max_length}> characters.")
        return v

    @field_validator("birth_date")
    @classmethod
    def check_birth_date(cls, v) -> date:
        min_date = datetime(1900, 1, 1)
        today = datetime.combine(date.today(), datetime.min.time())
        if v and v < min_date:
            raise ValueError(f"Birth date must be after {min_date.strftime('%Y-%m-%d')}.")
        elif v and v > today:
            raise ValueError(f"Birth date cannot be after {today.strftime('%Y-%m-%d')}.")
        elif v and v >= min_date:
            print(f"OK! Birth date is {v}.")
        else:
            print(f"NOT OK! Birth date is {v}.")
        return v
