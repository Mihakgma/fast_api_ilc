from datetime import datetime
from typing import List, Union

from pydantic import BaseModel
from pydantic.v1 import validator


class User(BaseModel):
    id = 0

    id: int
    first_name: str = "Иван"
    surname: str = "Иванович"
    last_name: str = "Иванов"
    birth_date: Union[datetime, None] = None
    email: str = "ivan_ivanch@sibir.ru"
    password: str = "1234"
    phone: str = "0123456789"
    department: str = "OKG"
    roles: List[int] = [1, 2, 3]
    info: str = "some information"

    @classmethod
    def get_id(cls):
        cls.next_id = getattr(cls, 'next_id', 0) + 1
        return cls.next_id

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, 'id'):  # This handles the cases where the id is not provided
            self.id = self.__class__.get_id()

    @validator("first_name")
    def check_first_name_length(self, v):
        if len(v) > 50:  # Adjust 50 as needed
            raise ValueError("First name must be at most 50 characters.")
        return v

    @validator("birth_date")
    def check_birth_date(self, v):
        min_date = datetime(1900, 1, 1)  # Adjust as needed
        if v and v < min_date:
            raise ValueError(f"Birth date must be after {min_date.strftime('%Y-%m-%d')}.")
        elif v and v >= min_date:
            print("OK")
            print(f"Birth date is {v}.")
        else:
            print("NOT OK")
            print(f"Birth date is {v}.")
        return v
