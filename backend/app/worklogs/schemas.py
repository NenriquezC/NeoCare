from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import date, datetime
from typing import Optional

class WorklogBase(BaseModel):
    date: date
    hours: float = Field(..., gt=0, description="Hours must be greater than 0")
    note: Optional[str] = Field(None, max_length=200)

    @field_validator('date')
    @classmethod
    def date_not_future(cls, v):
        if v > date.today():
            raise ValueError('Date cannot be in the future')
        return v

    @field_validator('hours')
    @classmethod
    def hours_minimum(cls, v):
        if v < 0.25:
            raise ValueError('Minimum hours allowed is 0.25')
        return v

class WorklogCreate(WorklogBase):
    pass

class WorklogUpdate(BaseModel):
    date: Optional[date] = None
    hours: Optional[float] = Field(None, gt=0)
    note: Optional[str] = Field(None, max_length=200)

    @field_validator('date')
    @classmethod
    def date_not_future(cls, v):
        if v and v > date.today():
            raise ValueError('Date cannot be in the future')
        return v

    @field_validator('hours')
    @classmethod
    def hours_minimum(cls, v):
        if v is not None and v < 0.25:
            raise ValueError('Minimum hours allowed is 0.25')
        return v

class WorklogOut(WorklogBase):
    id: int
    user_id: int
    card_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
