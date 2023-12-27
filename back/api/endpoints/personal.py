from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm


import sys

from service.personal import Personal
from models.user import User
from service.auth import get_current_user

router = APIRouter(
    prefix='/personal',
    tags=['personal'],
)


@router.get('/get_user')
async def get_user(
        personal_id: int,
        service: Personal = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.get_one(personal_id, current_user.id)


@router.get('/get_all')
async def get_all(
        service: Personal = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.get_all(current_user.id)


@router.get('/worker_day_visits')
async def get_all(
        personal_id: int,
        date: str,
        service: Personal = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.worker_day_visits(personal_id,date,current_user.id)

@router.get('/worker_day_visits_pos')
async def get_all(
        personal_id: int,
        date: str,
        pos_boolean: bool,
        service: Personal = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.worker_day_visits_pos(personal_id,date,pos_boolean,current_user.id)

@router.get('/get_personal_faces')
async def get_all(
        personal_id: int,
        service: Personal = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.get_personal_faces_ids(personal_id,current_user.id)

@router.get('/get_single_faces')
async def get_all(
        face_id: int,
        service: Personal = Depends(),
        current_user: User = Depends(get_current_user),
):
    return service.get_single_face(face_id,current_user.id)

