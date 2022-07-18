from peewee import *
from playhouse.db_url import connect
from opensocial.config import ConfigAPI

database = connect(ConfigAPI.database)

class BaseModel(Model):
    class Meta:
        database = database