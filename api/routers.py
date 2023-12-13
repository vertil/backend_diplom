from fastapi import APIRouter

from .endpoints.auth import router as auth_router
from .endpoints.machine import router as machine_router
from .endpoints.departments import router as department_router
from .endpoints.personal import router as personal_router


router = APIRouter(
    prefix='/api',
    tags=['api'],
)


router.include_router(auth_router)
router.include_router(machine_router)
router.include_router(department_router)
router.include_router(personal_router)