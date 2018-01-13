from django.conf import settings
from django.contrib.auth import get_user_model
from validate_email import validate_email
from django.utils.crypto import get_random_string

import requests
import datetime

class EmailOrUsernameModelBackend(object):
    """
    This is a ModelBackend that allows authentication with either a username or an email address.

    """
    def authenticate(self, username=None, password=None):
        User = get_user_model()
        if validate_email(username):
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None

class FacebookAuthorizationBackend(object):
    """
    This is a ModelBackend that allows authentication with facebook access token.

    """
    def authenticate(self, username=None, password=None):
        User = get_user_model()
        url = 'https://graph.facebook.com/v2.11/me?fields=id,name,email,birthday'
        access_token = 'Bearer ' + username
        response = requests.get(url, headers={'Authorization':access_token}).json()
        if 'id' in response:
            try:
                user = User.objects.get(email=response['email'])
            except User.DoesNotExist:
                user = User.objects.create(
                    username=response['email'],
                    email=response['email'],
                    name=response['name'],
                    birth_date=datetime.datetime.strptime(response['birthday'], "%m/%d/%Y").strftime("%Y-%m-%d"),
                    password=get_random_string(length=32)
                )
            return user
        else:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None
