from pydantic import BaseModel, EmailStr, Field

from app.classes.id_maker import IdMaker


class Department(BaseModel):
    id: int = IdMaker.get_id("Department")
    code: str = ""
    name: str = ""
    phone: str = "0123456789"
    email: EmailStr | None = Field(default=None)
    head_id: int = Field(default=None)

    def __str__(self):
        return f"{self.code} - {self.name}"
