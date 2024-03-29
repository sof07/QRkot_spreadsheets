from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.projects import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
    charity_project_name: str,
    session: AsyncSession,
) -> None:
    charity_project_id = await charity_project_crud.get_charity_project_id_by_name(
        charity_project_name, session
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Проект с таким именем уже существует!",
        )


async def project_is_closed(
    project_id: int,
    sesion: AsyncSession,
) -> None:
    """Проверяет не закрыт ли проект."""
    charity_project = await charity_project_crud.get(project_id, sesion)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!",
        )


async def check_amount(
    project_id: int, full_amount: int, session: AsyncSession
) -> None:
    """Валидация поля full_amount."""
    charity_project = await charity_project_crud.get(project_id, session)
    if full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нелья установить значение full_amount меньше уже вложенной суммы.",
        )


async def check_project(
    project_id: int,
    sesion: AsyncSession,
) -> CharityProject:
    """Проверяет наличие проекта в базе данных."""
    charity_project = await charity_project_crud.get(project_id, sesion)
    if not charity_project:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Проект не найден"
        )
    return charity_project


async def check_the_invested_funds(
    project: CharityProject,
) -> None:
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!",
        )
