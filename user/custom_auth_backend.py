from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from validate_email import validate_email

import requests
import datetime

User = get_user_model()


class EmailOrUsernameModelBackend(object):
    """
    This is a ModelBackend that allows authentication
    with either a username or an email address.

    """

    def authenticate(self, username=None, password=None):
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
            return User.objects.get(pk=username)
        except User.DoesNotExist:
            return None


class FacebookAuthorizationBackend(object):
    """
    This is a ModelBackend that allows
    authentication with facebook access token.

    """

    def authenticate(self, username=None, password=None):
        url = 'https://graph.facebook.com/v2.11/me?fields=id,name,email,birthday'
        access_token = 'Bearer ' + username
        response = requests.get(
            url, headers={'Authorization': access_token}).json()
        if 'id' in response:
            try:
                user = User.objects.get(email=response['email'])
            except User.DoesNotExist:
                user = User.objects.create(
                    username=response['email'],
                    email=response['email'],
                    name=response['name'],
                    birth_date=datetime.datetime.strptime(
                        response['birthday'], "%m/%d/%Y").strftime("%Y-%m-%d"),
                    password=get_random_string(length=32)
                )
            return user
        else:
            return None

    def get_user(self, username):
        try:
            return User.objects.get(pk=username)
        except User.DoesNotExist:
            return None
