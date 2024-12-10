from typing import Dict

# from fastapi.dependencies import models
from pydantic import BaseModel, Field

from app.classes.id_maker import IdMaker
from app.models.department import Department


class AdditionalInfo(BaseModel):
    id: int = IdMaker.get_id("AdditionalInfo")
    info_details: Dict[Department, str] = Field(default_factory=dict)
