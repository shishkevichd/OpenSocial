from datetime import datetime
import secrets
from peewee import *
from opensocial.api.accounts import Accounts
from opensocial.model import BaseModel
from opensocial.utilities import UtilitiesAPI


class Groups(BaseModel):
    id = IntegerField(primary_key=True)
    create_time = DateTimeField(default=datetime.utcnow)
    group_id = CharField(15)
    group_name = CharField(64, null=False)
    group_status = CharField(256, null=True)
    meta_web = TextField(null=True)
    meta_address = TextField(null=True)
    meta_phone_number = CharField(24, null=True)

    def getJSON(self, advanced=False):
        json_object = {
            'group_id': self.group_id,
            'group_name': self.group_name,
            'group_status': self.group_status if self.group_status else None,
            'meta': {
                'meta_web': self.meta_web if self.meta_web else None,
                'meta_address': self.meta_address if self.meta_address else None,
                'meta_phone_number': self.meta_phone_number if self.meta_phone_number else None
            }
        }

        if advanced:
            json_object['posts'] = [post.getJSON() for post in self.posts]
        
        return json_object

    def createGroup(access_token, group_name):
        from opensocial.api.subscribers import Subscribers

        createGroupErrors = [
            'invalid_token',
            'short_group_name'
        ]

        if Accounts.isValidAccessToken(access_token):
            if len(group_name) > 2:
                new_group_id = secrets.token_hex(7)

                Groups.create(
                    group_name=group_name,
                    group_id=new_group_id
                )

                Subscribers.create(
                    subscriber=Accounts.get(Accounts.access_token == access_token),
                    subscribed_at=Groups.get(Groups.group_id == new_group_id),
                    status='owner'
                )

                return {
                    'status': True
                }
            else:
                return UtilitiesAPI.errorJson(createGroupErrors[1])
        else:
            return UtilitiesAPI.errorJson(createGroupErrors[0])

    def createPost(access_token, group_id, content):
        from opensocial.api.subscribers import Subscribers
        from opensocial.api.posts import Posts

        createPostErrors = [
            "invalid_token",
            "group_not_found",
            "access_denied",
            "short_content"
        ]

        if Accounts.isValidAccessToken(access_token):
            target_group = Groups.get_or_none(Groups.group_id == group_id)
            creator_user = Accounts.get(Accounts.access_token == access_token)

            if target_group != None:
                poster = Subscribers.get_or_none(Subscribers.subscriber == creator_user)

                if poster != None and poster.status != 'user':
                    if len(content) >= 1:
                        new_post_id = secrets.token_hex(8)
                   
                        Posts.create(
                            group_creator=target_group,
                            group_created_by=creator_user,
                            content=content,
                            post_id=new_post_id
                        )

                        return {
                            'status': True,
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

    def deletePost(access_token, group_id, post_id):
        from opensocial.api.subscribers import Subscribers
        from opensocial.api.posts import Posts

        deletePostErrors = [
            "invalid_token",
            "group_not_found",
            "access_denied",
            "post_not_found"
        ]

        if Accounts.isValidAccessToken(access_token):
            target_group = Groups.get_or_none(Groups.group_id == group_id)
            creator_user = Accounts.get(Accounts.access_token == access_token)

            if target_group != None:
                poster = Subscribers.get_or_none(Subscribers.subscriber == creator_user)

                if poster != None and poster.status != 'user':
                    target_post = Posts.get_or_none(Posts.post_id == post_id)

                    if target_post != None:
                        target_post.delete_instance()

                        return {
                            'status': True
                        }
                    else:
                        return UtilitiesAPI.errorJson(deletePostErrors[3])
                else:
                    return UtilitiesAPI.errorJson(deletePostErrors[2])
            else:
                return UtilitiesAPI.errorJson(deletePostErrors[1])
        else:
            return UtilitiesAPI.errorJson(deletePostErrors[0])

    def editPost(access_token, group_id, post_id, content):
        from opensocial.api.subscribers import Subscribers
        from opensocial.api.posts import Posts

        editPostErrors = [
            "invalid_token",
            "group_not_found",
            "access_denied",
            "post_not_found"
        ]

        if Accounts.isValidAccessToken(access_token):
            target_group = Groups.get_or_none(Groups.group_id == group_id)
            editor = Accounts.get(Accounts.access_token == access_token)

            if target_group != None:
                poster = Subscribers.get_or_none(
                    Subscribers.subscriber == editor,
                    Subscribers.subscribed_at == target_group
                )

                if poster != None and poster.status != 'user':
                    target_post = Posts.get_or_none(Posts.post_id == post_id)

                    if target_post != None:
                        target_post.content = content
                        target_post.is_edited = True
                        target_post.edit_time = datetime.utcnow()

                        target_post.save()

                        return {
                            'status': True
                        }
                    else:
                        return UtilitiesAPI.errorJson(editPostErrors[3]) 
                else:
                    return UtilitiesAPI.errorJson(editPostErrors[2])
            else:
                return UtilitiesAPI.errorJson(editPostErrors[1])
        else:
            return UtilitiesAPI.errorJson(editPostErrors[0])

    def setUserGroupRole(access_token, group_id, user_id, status):
        from opensocial.api.subscribers import Subscribers

        setUserGroupStatusErrors = [
            'invalid_token',
            'group_not_found',
            'user_not_found',
            'user_not_subscribed',
            'access_denied',
            'use_group_transferowner_method',
            'invalid_status'
        ]

        if Accounts.isValidAccessToken(access_token):
            target_group = Groups.get_or_none(Groups.group_id == group_id)
            target_user = Accounts.get_or_none(Accounts.user_id == user_id)
            target_user_change = Subscribers.get_or_none(
                Subscribers.subscriber == target_user,
                Subscribers.subscribed_at == target_group
            )

            if target_group != None:
                if target_user != None:
                    if target_user_change != None:
                        role_changer = Subscribers.get_or_none(
                            Subscribers.subscriber == Accounts.get(Accounts.access_token == access_token),
                            Subscribers.subscribed_at == target_group
                        )

                        if role_changer != None and role_changer.status == 'admin' or role_changer.status == 'owner':
                            if status == 'editor' or status == 'admin' or status == 'user':
                                target_user_change.status = status

                                target_user_change.save()

                                return {
                                    'status': True
                                }
                            elif status == 'owner' and role_changer.status == 'owner':
                                return UtilitiesAPI.errorJson(setUserGroupStatusErrors[5])
                            else:
                                return UtilitiesAPI.errorJson(setUserGroupStatusErrors[6])
                        else:
                            return UtilitiesAPI.errorJson(setUserGroupStatusErrors[4])
                    else:
                        return UtilitiesAPI.errorJson(setUserGroupStatusErrors[3])
                else:
                    return UtilitiesAPI.errorJson(setUserGroupStatusErrors[2])
            else:
                return UtilitiesAPI.errorJson(setUserGroupStatusErrors[1])
        else:
            return UtilitiesAPI.errorJson(setUserGroupStatusErrors[0])

    def subscribeAtGroup(access_token, group_id):
        from opensocial.api.subscribers import Subscribers

        subscribeAtGroupErrors = [
            'invalid_token',
            'group_not_found',
            'you_already_subscribed'
        ]

        if Accounts.isValidAccessToken(access_token):
            target_group = Groups.get_or_none(Groups.group_id == group_id)

            if target_group != None:
                is_subscribed = Subscribers.get_or_none(
                    Subscribers.subscriber == Accounts.get(Accounts.access_token == access_token),
                    Subscribers.subscribed_at == target_group
                )

                if is_subscribed == None:
                    Subscribers.create(
                        subscriber=Accounts.get(Accounts.access_token == access_token),
                        subscribed_at=target_group
                    )

                    return {
                        'status': True
                    }
                else:
                    return UtilitiesAPI.errorJson(subscribeAtGroupErrors[2])
            else:
                return UtilitiesAPI.errorJson(subscribeAtGroupErrors[1])
        else:
            return UtilitiesAPI.errorJson(subscribeAtGroupErrors[0])

    def unsubscribeFromGroup(access_token, group_id):
        from opensocial.api.subscribers import Subscribers

        unsubscribeFromGroupErrors = [
            'invalid_token',
            'group_not_found',
            'you_arent_subscribed',
            'you_are_group_owner'
        ]

        if Accounts.isValidAccessToken(access_token):
            target_group = Groups.get_or_none(Groups.group_id == group_id)

            if target_group != None:
                is_subscribed = Subscribers.get_or_none(
                    Subscribers.subscriber == Accounts.get(Accounts.access_token == access_token),
                    Subscribers.subscribed_at == target_group
                )

                if is_subscribed != None:
                    if is_subscribed.status != 'owner':
                        is_subscribed.delete_instance()

                        return {
                            'status': True
                        }
                    else:
                        return UtilitiesAPI.errorJson(unsubscribeFromGroupErrors[3]) 
                else:
                    return UtilitiesAPI.errorJson(unsubscribeFromGroupErrors[2])
            else:
                return UtilitiesAPI.errorJson(unsubscribeFromGroupErrors[1])
        else:
            return UtilitiesAPI.errorJson(unsubscribeFromGroupErrors[0])