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


def add_init_vms():

    session = get_session()

    #get ini machines names from db
    try:
        ans = session.query(MachineTempInitlDB).all()
    except Exception as e:
        logging.error(f"error can't get init vms in db: {e}")
        print(f"error can't get init vms in db: {e}")
        sys.exit()

    if type(ans) != list:
        logging.error(f"init vm list from db is not list")
        print(f"init vm list from db is not list")
        sys.exit()

    if len(ans) == 0:
        logging.error(f"init vm list from db is empty")
        print(f"init vm list from db is empty")
        sys.exit()

    vms_db_names = {}
    for i in ans:
        vms_db_names[i.name]=0

    try:
        conn = ProxmoxAPI(settings.proxmox_path, user=settings.proxmox_user, password=settings.proxmox_password,
                          verify_ssl=False)
    except Exception as e:
        logging.error(f"can't get proxmox connection")
        print(f"can't get proxmox connection")
        sys.exit()


    try:            
        nodes = conn.nodes().get()        
    except Exception as e:
        print(f"can't get node list: {e}")
        logging.error(f"can't get node list for init_vms: {e}")
        sys.exit()


    try:
        for node in nodes:
            #get vms from node
            vms = conn.nodes(node['node']).qemu().get()

            #convert to listof names
            names = []            
            for vm in vms:
                names.append(vm['name'])

            #check is node have init vms
            for name, amount in vms_db_names.items():
                
                matches = names.count(name)
                   
                if matches == 1:
                    vms_db_names[name] = vms_db_names[name]+1
                    continue
                elif matches > 1:
                    print(f"{name} have several copies on node {node['node']}")
                    logging.error(f"{name} have several copies on node {node['node']}")
                    sys.exit()
 
    except Exception as e:
        print(f"can't check init_vms in proxmox")
        logging.error(f"can't check init_vms in proxmox")
        sys.exit()


    for name, amount in vms_db_names.items():
        if amount == 0:
            continue
        else:
            print(f"alredy exist {name}")
            logging.error(f"alredy exist {name}")
            return

    
    creator.create_init_machines(session)

    print(f"succesfull created init vms")
    logging.error(f"succesfull created init vms")


if __name__ == "__main__":
    

    add_default_user()

    #create init machines, but work with bugs need rework
    #add_init_vms()

    uvicorn.run(
        "core:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )
