from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.responses import JSONResponse
from passlib.hash import bcrypt
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from redis import Redis
from sqlalchemy.exc import SQLAlchemyError
import logging


from fastapi.security import OAuth2PasswordBearer

from database.db_connector import get_session
from database.redis_connector import get_redis_session
from schemas.userdb import UserDB, TokenHistory
from models.user import User, UserCreate
from models.token import Token
from settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/auth/sign-in')


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return AuthService.validate_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={
                'WWW-Authenticate': 'Bearer'
            },
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
            user_data = payload.get('user')
            if user_data is None:

                raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        except jwt.ExpiredSignatureError:
            print("jwt.ExpiredSignatureError")
            raise exception from None
        except JWTError:
            print("JWTError")
            raise exception from None
        try:
            user = User.parse_obj(user_data)
        except ValidationError:
            print("ValidationError")
            raise exception from None
        # Добавить проверку существования токена в редис, если всё ок обновить время существования
        if get_redis_session().get(user.id):
            get_redis_session().set(user.id, token, ex=settings.jwt_expiration)
            get_redis_session().expire(user.id, settings.jwt_expiration)
            return user
        else:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    @classmethod
    def create_token(cls, user: UserDB) -> Token:
        user_data = User.from_orm(user)

        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expiration),
            'sub': str(user_data.id),
            'user': user_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        hist_token = TokenHistory(
            username=user_data.username,
            token=token,
        )
        #  Добавить добовление токена в БД для истории
        try:
            get_session().add(hist_token)
            get_session().commit()
        except SQLAlchemyError:
            raise HTTPException(status_code=400, detail="User create token failed")
        return Token(access_token=token)

    def __init__(self,
                 session_db: Session = Depends(get_session),
                 session_redis: Redis = Depends(get_redis_session)
                 ):
        self.session_redis = session_redis
        self.session = session_db

    def register_new_user(self, user_data: UserCreate) -> JSONResponse:
        try:
            user = UserDB(
                email=user_data.email,
                username=user_data.username,
                hashed_password=self.hash_password(user_data.password),
                description=user_data.description
            )
            self.session.add(user)
            self.session.commit()
        except SQLAlchemyError as e:
            logging.error(f"User {user.username} registration failed: \n {e}")
            raise HTTPException(status_code=400, detail=f"User registration failed: \n {e}")
        # t = self.create_token(user)
        logging.info(f"User {user.username} successfully registered")
        return JSONResponse(content={"message": "User {user.username} successfully registered"}, status_code=200)

    def authenticate_user(self, username: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password!',
            headers={
                'WWW-Authenticate': 'Bearer'
            },
        )
        try:
            user = (
                self.session.query(UserDB).filter(UserDB.username == username).first()
            )
        except Exception as e:

            logging.error(f"authenticate_user {username}: can't get connect to DB")
            raise HTTPException(status_code=400, detail=f"can't get connect to DB")


        if not user or not self.verify_password(password, user.hashed_password):
            logging.error(f"authenticate_user:{exception}")
            raise exception
        else:
            # it'll create new token if user exist
            new_token = self.create_token(user)
            # it'll save token to redis if user exist
            self.session_redis.set(user.id, str(new_token), ex=settings.jwt_expiration)
            #return Token(access_token=new_token)

            return new_token

    def logout_user(self, user: User) -> JSONResponse:
        try:
            self.session_redis.delete(user.id)

            headers = {"Cache-Control": "no-store"}
            logging.info(f"logout user {user.username} successfully")
            return JSONResponse(status_code=200, headers=headers, content={"message": "Logged out successfully."})

        except JWTError:
            logging.error(f"logout user {user.username} bad token")
            return JSONResponse(status_code=401, headers=headers, content={"message": "Bad Token"})

