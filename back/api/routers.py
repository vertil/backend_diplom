from fastapi import APIRouter

from .endpoints.auth import router as auth_router
from .endpoints.departments import router as department_router
from .endpoints.personal import router as personal_router
from .endpoints.cameras import router as cameras_router
from .endpoints.cabinets import router as cabinets_router
from .endpoints.in_out_status import router as in_out_status_router
from .endpoints.undef_faces import router as undef_faces_router



router = APIRouter(
    prefix='/api',
    tags=['api'],
)


router.include_router(auth_router)
router.include_router(department_router)
router.include_router(personal_router)
router.include_router(cameras_router)
router.include_router(cabinets_router)
router.include_router(in_out_status_router)
router.include_router(undef_faces_router)