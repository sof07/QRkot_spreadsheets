from fastapi import APIRouter

from app.api.endpoints import (
    donations_router,
    projects_router,
    user_router,
    google_api_router,
)

main_router = APIRouter()
main_router.include_router(donations_router, prefix="/donation", tags=["Donation"])
main_router.include_router(
    projects_router, prefix="/charity_project", tags=["CharityProject"]
)
main_router.include_router(user_router)
main_router.include_router(google_api_router, prefix="/google", tags=["Google"])
