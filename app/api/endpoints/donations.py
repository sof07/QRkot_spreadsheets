from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donations import donation_crud
from app.models import Donation, User
from app.schemas.donations import DonationsCreate, DonationsDB, DonationMY
from app.services.services import invest_after_project_creation

router = APIRouter()


@router.post(
    "/",
    response_model=DonationMY,
)
async def create_new_donation(
    donation: DonationsCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> Donation:
    """Только для суперюзеров."""
    new_donation = await donation_crud.create(donation, session, user)
    await invest_after_project_creation(session, Donation)
    return new_donation


@router.get(
    "/",
    response_model=list[DonationsDB],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
) -> Donation:
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    "/my",
    response_model=list[DonationMY],
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> Donation:
    """Получает список всех донатов для текущего пользователя."""
    reservations = await donation_crud.get_by_user(session=session, user=user)
    return reservations
