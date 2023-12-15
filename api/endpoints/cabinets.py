from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm


import sys

from service.cabinets import Cabinets
from models.user import User
from service.auth import get_current_user

router = APIRouter(
    prefix='/cabinets',
    tags=['cabinets'],
)

@router.get('/get_cab')
async def get_user(
        cabinet_id: int,
        service: Cabinets = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.get_one(cabinet_id, current_user.id)


@router.get('/get_all')
async def get_all(
        service: Cabinets = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.get_all(current_user.id)

@router.get('/cab_visits')
async def get_all(
        cab_id: int,
        date: str,
        service: Cabinets = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.cab_visits(cab_id, date, current_user.id)

