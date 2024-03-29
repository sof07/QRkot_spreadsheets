from typing import Optional

from sqlalchemy import select
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


charity_project_crud = CRUDCharityProject(CharityProject)
