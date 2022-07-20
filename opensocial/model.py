from peewee import *
from playhouse.db_url import connect
from opensocial.config import ConfigAPI

import json


database = connect(ConfigAPI.database)


class BaseModel(Model):
    class Meta:
        database = database


class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)