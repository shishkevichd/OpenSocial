from peewee import *
from opensocial.model import BaseModel
from opensocial.api.accounts import Accounts
from opensocial.utilities import UtilitiesAPI


class Friends(BaseModel):
    id = IntegerField(primary_key=True)
    first_friend = ForeignKeyField(Accounts, backref='outcoming_friends')
    second_friend = ForeignKeyField(Accounts, backref='incoming_friends')
    status = CharField(16, default='incoming')

    def sendRequest(access_token, user_id):
        sendRequestErrors = [
            "incorrect_token",
            "user_not_found",
            "request_already_sent",
            "its_the_same_request",
            "cant_send_request_to_yourself"
        ]

        if Accounts.isValidAccessToken(access_token):
            is_sent_request_to_yourself = Accounts.get(Accounts.access_token == access_token)

            if is_sent_request_to_yourself.user_id != user_id:
                is_target_friend_avaliable = Accounts.get_or_none(Accounts.user_id == user_id)

                if is_target_friend_avaliable != None:
                    is_request_already_send = Friends.get_or_none(
                        Friends.first_friend == Accounts.get(Accounts.access_token == access_token), 
                        Friends.second_friend == Accounts.get(Accounts.user_id == user_id)
                    )

                    if is_request_already_send == None:
                        is_not_the_same_request = Friends.get_or_none(
                            Friends.first_friend == Accounts.get(Accounts.user_id == user_id), 
                            Friends.second_friend == Accounts.get(Accounts.access_token == access_token)
                        )

                        if is_not_the_same_request == None:
                            Friends.create(
                                first_friend=Accounts.get(Accounts.access_token == access_token),
                                second_friend=Accounts.get(Accounts.user_id == user_id)
                            )

                            return {
                                'status': True
                            }
                        else:
                            return UtilitiesAPI.errorJson(sendRequestErrors[3])
                    else:
                        return UtilitiesAPI.errorJson(sendRequestErrors[2])
                else:
                    return UtilitiesAPI.errorJson(sendRequestErrors[1])
            else:
                return UtilitiesAPI.errorJson(sendRequestErrors[4]) 
        else:
            return UtilitiesAPI.errorJson(sendRequestErrors[0])
    
    def acceptRequest(access_token, user_id):
        acceptRequestErrors = [
            "incorrect_token",
            "user_not_found",
            "cant_accept_request_to_yourself",
            "there_was_no_request"
        ]

        if Accounts.isValidAccessToken(access_token):
            is_yourself = Accounts.get(Accounts.access_token == access_token)

            if is_yourself.user_id != user_id:
                is_user_avaliable = Accounts.get_or_none(Accounts.user_id == user_id)

                if is_user_avaliable != None:
                    target_friend_request = Friends.get_or_none(
                        Friends.first_friend == Accounts.get(Accounts.user_id == user_id),
                        Friends.second_friend == Accounts.get(Accounts.access_token == access_token)
                    )

                    if (target_friend_request != None and target_friend_request.status == 'incoming') or (target_friend_request != None and target_friend_request.status == 'declined'):
                        target_friend_request.status = 'accepted'
                        target_friend_request.save()

                        return {
                            'status': True
                        }
                    else:
                        return UtilitiesAPI.errorJson(acceptRequestErrors[3])
                else:
                    return UtilitiesAPI.errorJson(acceptRequestErrors[1])
            else:
                return UtilitiesAPI.errorJson(acceptRequestErrors[2])
        else:
            return UtilitiesAPI.errorJson(acceptRequestErrors[0])

    def declineRequest(access_token, user_id):
        declineRequestErrors = [
            "incorrect_token",
            "user_not_found",
            "cant_decline_request_to_yourself",
            "there_was_no_request"
        ]

        if Accounts.isValidAccessToken(access_token):
            is_yourself = Accounts.get(Accounts.access_token == access_token)

            if is_yourself.user_id != user_id:
                is_user_avaliable = Accounts.get_or_none(Accounts.user_id == user_id)

                if is_user_avaliable != None:
                    target_friend_request = Friends.get_or_none(
                        Friends.first_friend == Accounts.get(Accounts.user_id == user_id),
                        Friends.second_friend == Accounts.get(Accounts.access_token == access_token)
                    )

                    if target_friend_request != None and target_friend_request.status == 'incoming':
                        target_friend_request.status = 'declined'
                        target_friend_request.save()

                        return {
                            'status': True
                        }
                    else:
                        return UtilitiesAPI.errorJson(declineRequestErrors[3])
                else:
                    return UtilitiesAPI.errorJson(declineRequestErrors[1])
            else:
                return UtilitiesAPI.errorJson(declineRequestErrors[2])
        else:
            return UtilitiesAPI.errorJson(declineRequestErrors[0])
    
    def deleteFromFriends(access_token, user_id):
        deleteFromFriendsErrors = [
            "incorrect_token",
            "user_not_found",
            "cant_delete_yourself_from_friends",
            "friend_is_not_on_the_list"
        ]

        if Accounts.isValidAccessToken(access_token):
            is_yourself = Accounts.get(Accounts.access_token == access_token)

            if is_yourself.user_id != user_id:
                is_user_avaliable = Accounts.get_or_none(Accounts.user_id == user_id)

                if is_user_avaliable != None:
                    target_friend = Friends.get_or_none(
                        Friends.first_friend == Accounts.get_or_none(Accounts.user_id == user_id),
                        Friends.second_friend == Accounts.get(Accounts.access_token == access_token)
                    )

                    if target_friend != None:
                        target_friend.delete_instance()

                        return { "status": True }
                    else:
                        target_other_friend = Friends.get_or_none(
                            Friends.first_friend == Accounts.get(Accounts.access_token == access_token),
                            Friends.second_friend == Accounts.get_or_none(Accounts.user_id == user_id)
                        )

                        if target_other_friend != None:
                            target_other_friend.delete_instance()

                            return { "status": True }
                        else:
                            return UtilitiesAPI.errorJson(deleteFromFriendsErrors[3])
                else:
                    return UtilitiesAPI.errorJson(deleteFromFriendsErrors[1])
            else:
                return UtilitiesAPI.errorJson(deleteFromFriendsErrors[2])
        else:
            return UtilitiesAPI.errorJson(deleteFromFriendsErrors[0])