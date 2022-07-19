from datetime import datetime
from peewee import *
from opensocial.model import BaseModel
from opensocial.api.groups import Groups
from opensocial.api.accounts import Accounts


class Posts(BaseModel):
    id = IntegerField(primary_key=True)
    content = TextField()
    create_date = DateTimeField(default=datetime.utcnow)
    group_creator = ForeignKeyField(Groups, backref='posts', null=True)
    group_created_by = ForeignKeyField(Accounts, backref='group_posts', null=True)
    user_creator = ForeignKeyField(Accounts, backref='posts', null=True)
    post_id = CharField(16)
    is_edited = BooleanField(default=False, null=True)
    edit_time = DateTimeField(default=None, null=True)