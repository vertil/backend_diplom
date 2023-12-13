import sys, logging

from clickhouse_connect.driver.client import Client
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from passlib.hash import bcrypt
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from redis import Redis
from sqlalchemy.exc import SQLAlchemyError

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import or_

sys.path.append('../')

from database.redis_connector import get_redis_session
from database.db_connector import get_session
from  models.polygon import PolygonScheme
from schemas.polygon import PolygonDB, MachineDB

class Machine:
    def __init__(self, session_db: Client = Depends(get_session),
                 session_redis: Redis = Depends(get_redis_session)):
        self.session_db = session_db
        self.session_redis = session_redis

    def _request_to_db(self, query: str) -> Session:
        return self.session_db.query(query)

    def _check_user_in_redis(self, user_id: int) -> bool:
        if self.session_redis.get(user_id):
            return True


    def get_info(self, id: int, user_id: int):

        if self._check_user_in_redis(user_id) is None:
            logging.error(f"machine/get_info user_id={user_id} - Invalid authentication credentials")
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        try:
            answer = self.session_db.query(MachineDB).filter(MachineDB.id == id).first()
        except Exception as e:
            logging.error(f"machine/get_info machine_id={id} - can't get data from db: {e}")
            raise HTTPException(status_code=400, detail=f"can't get data from db: \n {e}")

        logging.info(f'machine/get_info machine_id={id} successfull')
        return JSONResponse(content=[jsonable_encoder(answer)], status_code=200)