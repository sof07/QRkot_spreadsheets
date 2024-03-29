from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import CharityProject, Donation


async def invest_after_project_creation(
    session: AsyncSession, model: Union[CharityProject, Donation]
):
    if model == CharityProject:
        item_type = CharityProject
        partner_type = Donation
    else:
        item_type = Donation
        partner_type = CharityProject
    open_items = await session.execute(
        select(item_type)
        .filter(item_type.fully_invested.is_(False))
        .order_by(item_type.create_date.desc())
    )
    open_items = open_items.scalars().first()

    open_partners = await session.execute(
        select(partner_type)
        .filter(partner_type.fully_invested.is_(False))
        .order_by(partner_type.create_date)
    )

    open_partners = open_partners.scalars().all()

    for partner in open_partners:
        remaining_funds_item = open_items.full_amount - open_items.invested_amount
        remaining_funds_partner = partner.full_amount - partner.invested_amount
        if open_items.full_amount >= remaining_funds_partner:
            open_items.invested_amount += remaining_funds_partner
            partner.fully_invested = (
                True  # повторяющийся блок, лучше уносить в отдельную функцию
            )
            partner.close_date = datetime.now()
            partner.invested_amount = partner.full_amount
        else:
            partner.invested_amount += remaining_funds_item
            open_items.fully_invested = True
            open_items.close_date = datetime.now()
            open_items.invested_amount = open_items.full_amount
        if open_items.full_amount == open_items.invested_amount:
            open_items.fully_invested = True
            open_items.close_date = datetime.now()

    await session.commit()
    await session.refresh(open_items)
