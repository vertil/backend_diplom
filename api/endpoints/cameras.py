from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm


import sys

from service.cameras import Cameras
from models.user import User
from service.auth import get_current_user

router = APIRouter(
    prefix='/cameras',
    tags=['cameras'],
)

@router.get('/get_all')
async def get_all(
        service: Cameras = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.get_all(current_user.id)

@router.get('/get_one')
async def get_all(
        cam_id: int,
        service: Cameras = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.get_one(cam_id,current_user.id)

@router.get('/get_cabinet_cameras')
async def get_all(
        cab_id: int,
        service: Cameras = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.get_cabinet_camers(cab_id,current_user.id)

