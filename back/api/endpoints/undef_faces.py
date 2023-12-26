from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm


import sys

from service.undef_faces import undef_faces
from models.user import User
from service.auth import get_current_user

router = APIRouter(
    prefix='/un_def_faces',
    tags=['un_def_faces'],
)

@router.get('/get_limit')
async def get_user(
        limit: int,
        service: undef_faces = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.get_limit(limit, current_user.id)

@router.get('/get_by_timestamp')
async def get_user(
        timestamp: str,
        service: undef_faces = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.get_by_timestamp(timestamp, current_user.id)