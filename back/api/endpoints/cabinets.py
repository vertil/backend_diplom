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

@router.get('/get_cabs_names')
async def get_all(
        service: Cabinets = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.get_cabs_names(current_user.id)

@router.get('/get_cabs_passages')
async def get_all(
        service: Cabinets = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.get_cabs_passages(current_user.id)

@router.get('/get_cabinet_per_ids')
async def get_all(
        cabinet_id: int,
        service: Cabinets = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.get_cabinet_per_ids(cabinet_id,current_user.id)

@router.get('/cab_visits')
async def get_all(
        cab_id: int,
        date: str,
        service: Cabinets = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.cab_visits(cab_id, date, current_user.id)

@router.get('/cab_visits_pos')
async def get_all(
        cab_id: int,
        date: str,
        pos_boolean: bool,
        service: Cabinets = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.cab_visits_pos(cab_id, date, pos_boolean, current_user.id)

@router.get('/pass_visits')
async def get_all(
        date: str,
        cab_id: int,
        pass_num: int,
        service: Cabinets = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.pass_visits(date, cab_id, pass_num, current_user.id)

@router.get('/pass_visits_pos')
async def get_all(
        date: str,
        cab_id: int,
        pass_num: int,
        pos_boolean: bool,
        service: Cabinets = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.pass_visits_pos(date, cab_id, pass_num, pos_boolean, current_user.id)