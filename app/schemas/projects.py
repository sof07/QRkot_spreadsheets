from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        title = "Класс проекта пожертвований"
        min_anystr_length = 1


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    pass

    class Config:
        title = "Схема обновления проекта пожертвований"
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: Optional[int] = Field(default=0)
    fully_invested: Optional[bool] = Field(default=False)
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
