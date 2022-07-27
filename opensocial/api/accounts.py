from datetime import datetime
from opensocial.model import BaseModel
from peewee import *
from werkzeug.security import generate_password_hash, check_password_hash
from opensocial.utilities import UtilitiesAPI

import re
import secrets


class Accounts(BaseModel):
    id = IntegerField(primary_key=True)
    email = CharField(max_length=50, null=False)
    password = TextField(null=False)
    first_name = CharField(max_length=50, null=False)
    last_name = CharField(max_length=50, null=False)
    join_date = DateTimeField(default=datetime.now)
    birthday = DateField(null=True)
    avatar = CharField(4096, null=True)
    user_id = CharField(max_length=12)
    gender = IntegerField(null=False)
    access_token = TextField(null=False)

    # ===================================
    # Auth
    # ===================================

    def login(user_email, user_password):
        loginErrors = [
            "incorrect_password_or_email"
        ]

        searchable_user = Accounts.get_or_none(Accounts.email == user_email)

        if searchable_user != None:
            if check_password_hash(searchable_user.password, user_password):
                return {
                    'success': True,
                    'data': {
                        'access_token': searchable_user.access_token,
                        'user_id': searchable_user.user_id
                    }
                }  
            else:
                return UtilitiesAPI.errorJson(loginErrors[0])
        else:
            return UtilitiesAPI.errorJson(loginErrors[0])

    def register(user_email, user_password, first_name, last_name, gender):
        registerErrors = [
            "incorrect_account_email",
            "incorrect_account_password",
            "incorrect_first_and_last_name",
            "incorrect_gender",
            "this_mail_already_exists"
        ]

        email_regex = r"^((\w[^\W]+)[\.\-]?){1,}\@(([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"
        
        is_email_already_exists = Accounts.get_or_none(Accounts.email == user_email)

        if is_email_already_exists == None:
            if bool(re.search(email_regex, user_email)):
                if UtilitiesAPI.password_check(user_password):
                    if len(first_name) > 2 and len(last_name) > 2:
                        if int(gender) == 1 or int(gender) == 2:
                            new_user_id = secrets.token_hex(8)
                            
                            Accounts.create(
                                email=user_email, 
                                password=generate_password_hash(user_password), 
                                first_name=first_name,
                                last_name=last_name,
                                gender=gender,
                                access_token=secrets.token_hex(24),
                                user_id=new_user_id,
                                avatar=f"https://avatars.dicebear.com/api/identicon/{new_user_id}.svg"
                            )

                            new_user = Accounts.get(Accounts.user_id == new_user_id)

                            return {
                                'success': True,
                                'data': {
                                    'access_token': new_user.access_token,
                                    'user_id': new_user.user_id
                                }
                            }
                        else:
                            return UtilitiesAPI.errorJson(registerErrors[3])
                    else:
                        return UtilitiesAPI.errorJson(registerErrors[2])
                else:
                    return UtilitiesAPI.errorJson(registerErrors[1])
            else:
                return UtilitiesAPI.errorJson(registerErrors[0])
        else:
            return UtilitiesAPI.errorJson(registerErrors[4])

    # ===================================
    # Posts
    # ===================================

    def createPost(access_token, content):
        from opensocial.api.posts import Posts

        return Posts.createPost(type='user', access_token=access_token, content=content)

    def deletePost(access_token, post_id):
        from opensocial.api.posts import Posts

        return Posts.deletePost(type='user', access_token=access_token, post_id=post_id)

    def editPost(access_token, post_id, content):
        from opensocial.api.posts import Posts

        return Posts.editPost(type='user', access_token=access_token, post_id=post_id, content=content)

    # ===================================
    # Gets
    # ===================================

    def getJSON(self, advanced=False):
        json_object = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': f"{self.first_name} {self.last_name}",
            'gender': 'man' if self.gender == 2 else "women",
            'user_id': self.user_id,
            'avatar_url': self.avatar
        }
        if advanced:
            json_object['join_date'] = self.join_date
            json_object['email'] = self.email

        return json_object

    def getUserPosts(access_token, user_id):
      getUserPostsErrors = [
        'invalid_token',
        'user_not_found'
      ]

      post_array = []
     
      if Accounts.isValidAccessToken(access_token):
        if user_id:
            target_user = Accounts.get_or_none(Accounts.user_id == user_id)

            if target_user != None:
                if target_user.posts.exists():
                    for post in target_user.posts:
                        post_array.append(post.getJSON())

                    return {
                        'success': True,
                        'data': post_array
                    }
                else:
                    return {
                        'success': True,
                        'data': post_array
                    }
            else:
                return UtilitiesAPI.errorJson(getUserPostsErrors[1])
        else:
            target_user = Accounts.get(Accounts.access_token == access_token)

            if target_user.posts.exists():
                for post in target_user.posts:
                    post_array.append(post.getJSON())

                return {
                    'success': True,
                    'data': post_array
                }
            else:
                return {
                    'success': True,
                    'data': post_array
                }
      else:
        return UtilitiesAPI.errorJson(getUserPostsErrors[0])

    def getPostCompilation(access_token):
        from opensocial.api.subscribers import Subscribers
        from opensocial.api.friends import Friends
        
        getPostCompilationErrors = [
            'invalid_token'
        ]
        
        if Accounts.isValidAccessToken(access_token):
            posts_array = []
            subscribed_groups = Subscribers.select().where(Subscribers.subscriber == Accounts.get(Accounts.access_token == access_token))

            if subscribed_groups.exists():
                for group in subscribed_groups:
                    group_posts = group.subscribed_at.posts

                    for group_post in group_posts:
                        posts_array.append(group_post.getJSON())

            friends_post = Friends.select().where((Friends.first_friend == Accounts.get(Accounts.access_token == access_token)) | (Friends.second_friend == Accounts.get(Accounts.access_token == access_token)))

            if friends_post.exists():
                for friend in friends_post:
                    if friend.first_friend == Accounts.get(Accounts.access_token == access_token):
                        friend_posts = friend.second_friend.posts
                    else:
                        friend_posts = friend.first_friend.posts

                    for friend_post in friend_posts:
                        posts_array.append(friend_post.getJSON())

            your_posts = Accounts.get(Accounts.access_token == access_token).posts

            for post in your_posts:
                posts_array.append(post.getJSON())

            return {
                'success': True,
                'data': posts_array
            }
        else:
            return UtilitiesAPI.errorJson(getPostCompilationErrors[0])

    def getUser(access_token, user_id):
        getUserErrors = [
            "invalid_token",
            "user_not_found"
        ]

        if Accounts.isValidAccessToken(access_token):
            if len(user_id) > 0:
                requested_user = Accounts.get_or_none(Accounts.user_id == user_id)
            
                if requested_user == None:
                    return UtilitiesAPI.errorJson(getUserErrors[1])
                else:
                    return {
                        'success': True,
                        'data': requested_user.getJSON()
                    }
            else:
                return {
                    'success': True,
                    'data': Accounts.get(Accounts.access_token == access_token).getJSON(advanced=True)
                }
        else:
            return UtilitiesAPI.errorJson(getUserErrors[0])

    def getSubscribedGroup(access_token, user_id=None):
        from opensocial.api.subscribers import Subscribers

        getSubscribedGroupErrors = [
            'invalid_token'
        ]
        
        if Accounts.isValidAccessToken(access_token):
            target_user = Accounts.get_or_none(Accounts.user_id == user_id)

            if target_user != None:
                user_groups = Subscribers.select(Subscribers.subscribed_at).where(Subscribers.subscriber == Accounts.get(Accounts.user_id == user_id))
            else:
                user_groups = Subscribers.select(Subscribers.subscribed_at).where(Subscribers.subscriber == Accounts.get(Accounts.access_token == access_token))

            groups_array = []

            if user_groups.exists():
                for group in user_groups:
                    groups_array.append(group.subscribed_at.getJSON(access_token=access_token))

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
            return UtilitiesAPI.errorJson(getSubscribedGroupErrors[0])
        
    # ===================================
    # Checker
    # ===================================

    def isValidAccessToken(target_access_token):
        requested_user = Accounts.get_or_none(Accounts.access_token == target_access_token)

        if requested_user == None:
            return False
        else:
            return True