from opensocial.model import BaseModel
from opensocial.api.posts import Posts
from peewee import *

import datetime


class Commentaries(BaseModel):
    id = IntegerField(primary_key=True)
    create_date = DateTimeField(default=datetime.datetime.utcnow)
    content = CharField(512)
    is_edited = BooleanField(default=False)
    parent_comment = ForeignKeyField('self', backref='childs', null=True)
    edit_date = DateTimeField(null=True)
    post = ForeignKeyField(Posts, backref='comments')
    comment_id = CharField(10)

    # ===================================
    # Gets
    # ===================================

    def getJSON(self):
        json_object = {
            'id': self.comment_id,
            'create_date': self.create_date,
            'content': self.content,
            'likes_count': len(self.likes),
            'child_comments': [comment.getJSON() for comment in self.childs],
            'edit_detail': {
                'is_edited': False,
                'edit_time': None
            }
        }

        if self.is_edited:
            json_object['edit_detail'] = {
                'is_edited': True,
                'edit_time': self.edit_date
            }

        return json_object