from pydantic import BaseSettings

import sys,os
#sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

class Settings(BaseSettings):
    
    server_host: str 
    server_port: int
    database_url: str 

    jwt_secret: str 
    jwt_algorithm: str 
    jwt_expiration: int 

    redis_url: str 

    proxmox_path: str
    proxmox_user: str
    proxmox_password: str
    max_instances: int 
    default_user: str
    default_user_pass: str
    default_user_descr: str
    default_user_email: str
    max_wgs: int

print(sys.path)

settings = Settings(
    _env_file='.env',
)


