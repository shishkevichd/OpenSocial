from peewee import *
from opensocial.model import BaseModel
from opensocial.api.accounts import Accounts
from opensocial.api.groups import Groups


class Subscribers(BaseModel):
    id = IntegerField(primary_key=True)
    subscriber = ForeignKeyField(Accounts, backref='subscribed_at')
    subscribed_at = ForeignKeyField(Groups, backref='subscribers')
    status = CharField(default='user')