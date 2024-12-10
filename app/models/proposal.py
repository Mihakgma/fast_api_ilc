from datetime import datetime
from typing import Union, Set

# from fastapi.dependencies import models
from pydantic import BaseModel

from app.models.additional_info import AdditionalInfo
from app.classes.id_maker import IdMaker
from app.models.department import Department
from app.models.eias_Number import EiasNumber
from app.models.protocol import Protocol
from app.models.user import User


class Proposal(BaseModel):
    """
    This class represents a proposal - application object (current row in the main DF)
    """
    id: int = IdMaker.get_id("Proposal")
    income_date: Union[datetime, None] = None
    act_code: str = None
    lab_code: str = None  # complex code from depts digit signs & date (month + year)
    sampling_date: Union[datetime, None] = None
    delivery_date: Union[datetime, None] = None
    sample_name: str = None
    sample_type_id: int = None
    creation_date: Union[datetime, None] = None
    applicant_id: int = None
    producer_id: int = None
    expiration_date: Union[datetime, None] = None
    research_type_id: int = None
    document_grounding_id: int = None
    applicant_document_number: int = None
    application_date: Union[datetime, None] = None
    applicant_document_expiration_date: Union[datetime, None] = None
    sender_id: int = None
    normative_document_id: int = None
    research_program: set() = None
    # autocompute : total probes
    sample_volume: dict = {"quantities": [],
                           "measurement_units": [],
                           "department": Department}
    sample_accepted_by: User = None
    protocols: Set[Protocol] = set()
    eias: EiasNumber = None
    notes: AdditionalInfo | None = None
