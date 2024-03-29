from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationsBase(BaseModel):
    comment: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        title = "Класс пользовательских пожертвований"
        min_anystr_length = 1


class DonationsCreate(DonationsBase):
    full_amount: int = Field(..., ge=1)


class DonationMY(DonationsBase):
    id: int
    create_date: datetime
    full_amount: int

    class Config:
        orm_mode = True


class DonationsDB(DonationMY):
    user_id: Optional[int]
    invested_amount: Optional[int] = Field(default=0)
    fully_invested: Optional[bool] = Field(default=False)
    close_date: Optional[datetime]
