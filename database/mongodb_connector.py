import sys

#sys.path.append('../')

import pymongo
from settings import settings




def create_client():
    client = pymongo.MongoClient(settings.mongoDB_url)
    return client

