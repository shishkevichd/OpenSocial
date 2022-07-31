from datetime import datetime
from faulthandler import is_enabled
import json
from peewee import *
from opensocial.model import BaseModel
from opensocial.api.groups import Groups
from opensocial.api.accounts import Accounts
from opensocial.utilities import UtilitiesAPI

import secrets


class Posts(BaseModel):
    id = IntegerField(primary_key=True)
    content = TextField()
    create_date = DateTimeField(default=datetime.utcnow)
    group_creator = ForeignKeyField(Groups, backref='posts', null=True)
    group_created_by = ForeignKeyField(Accounts, backref='group_posts', null=True)
    user_creator = ForeignKeyField(Accounts, backref='posts', null=True)
    post_id = CharField(16)
    is_edited = BooleanField(default=False, null=True)
    enabled_comments = BooleanField(default=True)
    edit_time = DateTimeField(default=None, null=True)

    # ===================================
    # Gets
    # ===================================

    def getJSON(self):
        jsonObject = {
            'post_id': self.post_id,
            'content': self.content,
            'create_datetime': self.create_date,
            'likes_count': len(self.likes),
        }

        if self.enabled_comments:
            jsonObject['comments'] = [comment.getJSON() for comment in self.comments]

        if self.is_edited:
            jsonObject['editData'] = {
                'isEdited': self.is_edited,
                'editDatetime': self.edit_time
            }

        if self.group_creator == None or self.group_created_by == None:
            jsonObject['creator'] = {
                'creator_type': 'user',
                'data': self.user_creator.getJSON()
            }
        else:
            jsonObject['creator'] = {
                'creator_type': 'group',
                'data': self.group_creator.getJSON()
            }

        return jsonObject

    # ===================================
    # Post manage
    # ===================================

    def createPost(type, **data):
        if type == 'group':
            from opensocial.api.subscribers import Subscribers
            from opensocial.api.posts import Posts

            createPostErrors = [
                "invalid_token",
                "group_not_found",
                "access_denied",
                "short_content"
            ]

            if Accounts.isValidAccessToken(data['access_token']):
                target_group = Groups.get_or_none(Groups.group_id == data['group_id'])
                creator_user = Accounts.get(Accounts.access_token == data['access_token'])

                if target_group != None:
                    poster = Subscribers.get_or_none(Subscribers.subscriber == creator_user)

                    if poster != None and poster.status != 'user':
                        if len(data['content']) >= 1:
                            new_post_id = secrets.token_hex(8)
                    
                            Posts.create(
                                group_creator=target_group,
                                group_created_by=creator_user,
                                content=data['content'],
                                post_id=new_post_id
                            )

                            return {
                                'success': True,
                                'data': {
                                    'post_id': new_post_id,
                                    'group_id': target_group.group_id
                                }
                            }
                        else:
                            return UtilitiesAPI.errorJson(createPostErrors[3]) 
                    else:
                        return UtilitiesAPI.errorJson(createPostErrors[2])
                else:
                    return UtilitiesAPI.errorJson(createPostErrors[1])
            else:
                return UtilitiesAPI.errorJson(createPostErrors[0])
        elif type == 'user':
            from opensocial.api.posts import Posts

            createPostErrors = [
                'invalid_token',
                'short_content'
            ]

            if Accounts.isValidAccessToken(data['access_token']):
                if len(data['content']) >= 1:
                    new_post_id = secrets.token_hex(8)
                    
                    Posts.create(
                        user_creator=Accounts.get(Accounts.access_token == data['access_token']),
                        content=data['content'],
                        post_id=new_post_id
                    )

                    return {
                        'success': True,
                        'data': {
                            'post_id': new_post_id
                        }
                    }
                else:
                    return UtilitiesAPI.errorJson(createPostErrors[1])
            else:
                return UtilitiesAPI.errorJson(createPostErrors[0])
        else:
            return False
    
    def deletePost(type, **data):
        if type == 'group':
            from opensocial.api.subscribers import Subscribers
            from opensocial.api.posts import Posts

            deletePostErrors = [
                "invalid_token",
                "group_not_found",
                "access_denied",
                "post_not_found"
            ]

            if Accounts.isValidAccessToken(data['access_token']):
                target_group = Groups.get_or_none(Groups.group_id == data['group_id'])
                creator_user = Accounts.get(Accounts.access_token == data['access_token'])

                if target_group != None:
                    poster = Subscribers.get_or_none(Subscribers.subscriber == creator_user)

                    if poster != None and poster.status != 'user':
                        target_post = Posts.get_or_none(Posts.post_id == data['post_id'])

                        if target_post != None:
                            target_post.delete_instance()

                            return {
                                'success': True
                            }
                        else:
                            return UtilitiesAPI.errorJson(deletePostErrors[3])
                    else:
                        return UtilitiesAPI.errorJson(deletePostErrors[2])
                else:
                    return UtilitiesAPI.errorJson(deletePostErrors[1])
            else:
                return UtilitiesAPI.errorJson(deletePostErrors[0])
        elif type == 'user':
            from opensocial.api.posts import Posts

            deletePostErrors = [
                'invalid_token',
                'post_not_found'
            ]

            if Accounts.isValidAccessToken(data['access_token']):
                target_post = Posts.get_or_none(
                    Posts.post_id == data['post_id'],
                    Posts.user_creator == Accounts.get(Accounts.access_token == data['access_token'])
                )

                if target_post != None:
                    target_post.delete_instance()

                    return {
                        'success': True
                    }
                else:
                    return UtilitiesAPI.errorJson(deletePostErrors[1])
            else:
                return UtilitiesAPI.errorJson(deletePostErrors[0])
        else:
            return False

    def editPost(type, **data):
        if type == 'group':
            from opensocial.api.subscribers import Subscribers
            from opensocial.api.posts import Posts

            editPostErrors = [
                "invalid_token",
                "group_not_found",
                "access_denied",
                "post_not_found",
                "short_content"
            ]

            if Accounts.isValidAccessToken(data['access_token']):
                target_group = Groups.get_or_none(Groups.group_id == data['group_id'])
                editor = Accounts.get(Accounts.access_token == data['access_token'])

                if target_group != None:
                    poster = Subscribers.get_or_none(
                        Subscribers.subscriber == editor,
                        Subscribers.subscribed_at == target_group
                    )

                    if poster != None and poster.status != 'user':
                        target_post = Posts.get_or_none(Posts.post_id == data['post_id'])

                        if target_post != None:
                            if len(data['content']) >= 1:
                                target_post.content = data['content']
                                target_post.is_edited = True
                                target_post.edit_time = datetime.utcnow()

                                target_post.save()

                                return {
                                    'success': True
                                }
                            else:
                                return UtilitiesAPI.errorJson(editPostErrors[4])
                        else:
                            return UtilitiesAPI.errorJson(editPostErrors[3]) 
                    else:
                        return UtilitiesAPI.errorJson(editPostErrors[2])
                else:
                    return UtilitiesAPI.errorJson(editPostErrors[1])
            else:
                return UtilitiesAPI.errorJson(editPostErrors[0])
        elif type == 'user':
            from opensocial.api.posts import Posts

            editPostErrors = [
                "invalid_token",
                "post_not_found",
                "short_content"
            ]

            if Accounts.isValidAccessToken(data['access_token']):
                target_post = Posts.get_or_none(
                    Posts.post_id == data['post_id'],
                    Posts.user_creator == Accounts.get(Accounts.access_token == data['access_token'])
                )

                if target_post != None:
                    if len(data['content']) >= 1:
                        target_post.content = data['content']
                        target_post.is_edited = True
                        target_post.edit_time = datetime.utcnow()

                        target_post.save()

                        return {
                            'success': True
                        }
                    else:
                        return UtilitiesAPI.errorJson(editPostErrors[2])
                else:
                    return UtilitiesAPI.errorJson(editPostErrors[1])
            else:
                return UtilitiesAPI.errorJson(editPostErrors[0])
        else:
            return False