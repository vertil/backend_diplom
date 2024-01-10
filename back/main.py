import uvicorn
import sys, os
import logging
#sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
from schemas.userdb import UserDB, TokenHistory
from database.db_connector import get_session
from settings import settings
from passlib.hash import bcrypt
from proxmoxer import ProxmoxAPI
from schemas.polygon import MachineTempInitlDB


level = logging.DEBUG
format_log = "%(asctime)s %(processName)s\%(name)-8s %(levelname)s: %(message)s"
if not os.path.exists("./logs/"):
    os.mkdir("./logs/")
logfile = "./logs/script.log"
logging.basicConfig(format=format_log, level=level, filename=logfile)
logger = logging.getLogger(__name__)


def add_default_user():
    session = get_session()

    try:
            
        ans = session.query(UserDB).filter(UserDB.username == settings.default_user).first()            
            
    except Exception as e:
        print(f"can't get db connection: {e}")        
        sys.exit()

    if ans == None:
        try:
            user = UserDB(
                email=settings.default_user_email,
                username=settings.default_user,
                hashed_password=bcrypt.hash(settings.default_user_pass),
                description=settings.default_user_descr                )
            session.add(user)
            session.commit()
        except Exception as e:
            logging.error(f"can't add default user: {e}")
            print(f"can't add default user: {e}")
    else:
        logging.info(f"default_user:{settings.default_user} alredy exist")
        print(f"default_user:{settings.default_user} alredy exist")


if __name__ == "__main__":
    

    add_default_user()

   
    uvicorn.run(
        "core:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )
