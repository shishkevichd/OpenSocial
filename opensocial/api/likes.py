import datetime

from opensocial.model import BaseModel
from opensocial.api.accounts import Accounts
from opensocial.api.posts import Posts
from opensocial.api.comments import Commentaries
from peewee import *

class Likes(BaseModel):
    id = IntegerField(primary_key=True)
    user = ForeignKeyField(Accounts, backref="liked")
    post = ForeignKeyField(Posts, backref="likes", null=True)
    comment = ForeignKeyField(Commentaries, backref="likes", null=True)
    like_date = DateTimeField(default=datetime.datetime.utcnow)