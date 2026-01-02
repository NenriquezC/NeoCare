from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from decimal import Decimal

class ReportSummary(BaseModel):
    completed: int
    overdue: int
    new: int

class UserHoursReport(BaseModel):
    user_id: int
    user_name: str
    total_hours: Decimal
    tasks_count: int

    model_config = ConfigDict(from_attributes=True)

class CardHoursReport(BaseModel):
    card_id: int
    title: str
    responsible: Optional[str]
    status: str
    total_hours: Decimal

    model_config = ConfigDict(from_attributes=True)
