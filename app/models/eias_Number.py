from pydantic import BaseModel

from app.classes.id_maker import IdMaker


class EiasNumber(BaseModel):
    id: int = IdMaker.get_id("EiasNumber")
    number: int = None
    inside_oa: bool = None
