from typing import Optional

from sqlalchemy import select, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_charity_project_id_by_name(
        self,
        fond_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_charity_project_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == fond_name)
        )
        db_charity_project_id = db_charity_project_id.scalars().first()
        return db_charity_project_id

    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> CharityProject:
        time_to_collect_funds = extract(
            "day", CharityProject.close_date - CharityProject.create_date
        ).label("days_to_collect")
        query = (
            select(CharityProject)
            .filter(CharityProject.fully_invested.is_(True))
            .order_by(time_to_collect_funds)
        )
        result = await session.execute(query)
        projects = result.scalars().all()
        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
