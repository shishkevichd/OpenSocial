from datetime import datetime
import secrets
from peewee import *
from opensocial.api.accounts import Accounts
from opensocial.model import BaseModel, JSONField
from opensocial.utilities import UtilitiesAPI


class Groups(BaseModel):
    id = IntegerField(primary_key=True)
    create_time = DateTimeField(default=datetime.utcnow)
    group_id = CharField(15)
    group_name = CharField(64, null=False)
    group_status = CharField(256, null=True)
    group_type = CharField(24, default='opened')
    avatar = CharField(4096, null=True)
    meta = JSONField(null=True)

    # ===================================
    # Group Manage
    # ===================================

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
                    group_id=new_group_id,
                    avatar=f"https://avatars.dicebear.com/api/identicon/{new_group_id}.svg"
                )

                Subscribers.create(
                    subscriber=Accounts.get(Accounts.access_token == access_token),
                    subscribed_at=Groups.get(Groups.group_id == new_group_id),
                    status='owner'
                )

                return {
                    'success': True
                }
            else:
                return UtilitiesAPI.errorJson(createGroupErrors[1])
        else:
            return UtilitiesAPI.errorJson(createGroupErrors[0])

    def createPost(access_token, group_id, content):
        from opensocial.api.posts import Posts

        return Posts.createPost(type='group', access_token=access_token, group_id=group_id, content=content)

    def deletePost(access_token, group_id, post_id):
        from opensocial.api.posts import Posts

        return Posts.deletePost(type='group', access_token=access_token, group_id=group_id, post_id=post_id)

    def editPost(access_token, group_id, post_id, content):
        from opensocial.api.posts import Posts

        return Posts.editPost(type='group', access_token=access_token, group_id=group_id, post_id=post_id, content=content)

    def deleteSubscriberFromGroup(access_token, group_id, user_id):
        from opensocial.api.subscribers import Subscribers 
        
        deleteSubscriberFromGroupErrors = [
            'invalid_token',
            'group_not_found',
            'user_not_found',
            'user_not_subscribed',
            'access_denied',
            'cant_delete_yourself'
        ]

        if Accounts.isValidAccessToken(access_token):
            target_group = Groups.get_or_none(Groups.group_id == group_id)
            target_user = Accounts.get_or_none(Accounts.user_id == user_id)

            if target_group != None:
                if target_user != None:
                    subscribedUser = Subscribers.get_or_none(
                        Subscribers.subscriber == target_user,
                        Subscribers.subscribed_at == target_group
                    )

                    isUserHasAccess = Subscribers.get_or_none(
                        Subscribers.subscriber == Accounts.get(Accounts.access_token == access_token),
                        Subscribers.subscribed_at == target_group
                    )

                    if subscribedUser != None:
                        if isUserHasAccess != None and isUserHasAccess.status == 'admin' or isUserHasAccess == 'owner':
                            isYourself = Accounts.get(Accounts.access_token == access_token)

                            if isYourself.user_id == user_id:
                                subscribedUser.delete_instance()

                                return {
                                    'success': True
                                }
                            else:
                                return UtilitiesAPI.errorJson(deleteSubscriberFromGroupErrors[5])
                        else:
                            return UtilitiesAPI.errorJson(deleteSubscriberFromGroupErrors[4])
                    else:
                        return UtilitiesAPI.errorJson(deleteSubscriberFromGroupErrors[3])
                else:
                    return UtilitiesAPI.errorJson(deleteSubscriberFromGroupErrors[2])
            else:
                return UtilitiesAPI.errorJson(deleteSubscriberFromGroupErrors[1])
        else:
            return UtilitiesAPI.errorJson(deleteSubscriberFromGroupErrors[0])

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
                                    'success': True
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

    # ===================================
    # Subscribe/unsubscribe from group
    # ===================================

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
                        'success': True
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
                            'success': True
                        }
                    else:
                        return UtilitiesAPI.errorJson(unsubscribeFromGroupErrors[3]) 
                else:
                    return UtilitiesAPI.errorJson(unsubscribeFromGroupErrors[2])
            else:
                return UtilitiesAPI.errorJson(unsubscribeFromGroupErrors[1])
        else:
            return UtilitiesAPI.errorJson(unsubscribeFromGroupErrors[0])

    # ===================================
    # Gets
    # ===================================

    def getJSON(self, advanced=False):
        json_object = {
            'group_id': self.group_id,
            'group_name': self.group_name,
            'group_status': self.group_status if self.group_status else None,
            'meta': self.meta if self.meta else None,
            'avatar_url': self.avatar
        }

        if advanced:
            json_object['posts'] = [post.getJSON() for post in self.posts]
        
        return json_object

    def searchGroup(access_token, query):
        searchGroupErrors = [
            'invalid_token',
            'short_query'
        ]

        groups_array = []
        
        if Accounts.isValidAccessToken(access_token):
            if len(query) > 0:
                group_query = Groups.select().where(Groups.group_name.contains(query) & Groups.group_type != 'local' | Groups.group_type != 'closed').limit(25)

                if group_query.exists():
                    for group in group_query:
                        groups_array.append(group.getJSON(access_token=access_token))

                    return {
                        'success': True,
                        'data': groups_array
                    }
                else:
                    return {
                        'success': True,
                        'data': groups_array
                    }
            else:
                return UtilitiesAPI.errorJson(searchGroupErrors[1])
        else:
            return UtilitiesAPI.errorJson(searchGroupErrors[0])

    def getGroup(access_token, group_id):
        from opensocial.api.subscribers import Subscribers

        getGroupErrors = [
            'invalid_token',
            'group_not_found',
            'closed_group',
            'invalid_type'
        ]

        if Accounts.isValidAccessToken(access_token):
            target_group = Groups.get_or_none(Groups.group_id == group_id)

            if target_group != None:
                if target_group.group_type == 'opened':
                    return target_group.getJSON()
                elif target_group.group_type == 'closed' or target_group.group_type == 'local':
                    is_user_subscribed = Subscribers.get_or_none(
                        Subscribers.subscriber == Accounts.get(Accounts.access_token == access_token),
                        Subscribers.subscribed_at == target_group
                    )

                    if is_user_subscribed != None:
                        return target_group.getJSON(access_token=access_token)
                    else:
                        if target_group.group_type == 'local':
                            return UtilitiesAPI.errorJson(getGroupErrors[2])
                        else:
                            return UtilitiesAPI.errorJson(getGroupErrors[1]) 
                else:
                    return UtilitiesAPI.errorJson(getGroupErrors[3])
            else:
                return UtilitiesAPI.errorJson(getGroupErrors[1])
        else:
            return UtilitiesAPI.errorJson(getGroupErrors[0])