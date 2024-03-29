from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_amount,
    check_name_duplicate,
    check_project,
    check_the_invested_funds,
    project_is_closed,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.projects import charity_project_crud
from app.models import CharityProject
from app.schemas.projects import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.services import invest_after_project_creation

router = APIRouter()


@router.post(
    "/",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(charity_project, session)
    await invest_after_project_creation(session, CharityProject)
    return new_charity_project


@router.get(
    "/",
    response_model=list[CharityProjectDB],
)
async def get_all_project(
    session: AsyncSession = Depends(get_async_session),
):
    all_rooms = await charity_project_crud.get_multi(session)
    return all_rooms


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project(project_id, session)
    await check_the_invested_funds(project)
    return project


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_reservation(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project(project_id, session)
    await project_is_closed(project_id, session)

    if obj_in.full_amount:
        await check_amount(project_id, obj_in.full_amount, session)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)

    reservation = await charity_project_crud.update(
        db_obj=project,
        obj_in=obj_in,
        session=session,
    )
    return reservation
