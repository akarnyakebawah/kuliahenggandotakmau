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
        if (len(username) <= 50):
            if validate_email(username):
                kwargs = {'email': username}
            else:
                kwargs = {'username': username}
            try:
                user = get_user_model().objects.get(**kwargs)
                if user.check_password(password):
                    return user
            except get_user_model().DoesNotExist:
                return None
        else:
            accessToken = 'Bearer ' + username
            response = requests.get('https://graph.facebook.com/v2.11/me?fields=id,name,email,birthday', headers={'Authorization':accessToken}).json()
            if ('id' in response):
                user = None
                try:
                    user = get_user_model().objects.get(email=response['email'])
                except get_user_model().DoesNotExist:
                    user = get_user_model().objects.create(
                        username=response['email'],
                        email=response['email'],
                        name=response['name'],
                        birth_date=datetime.datetime.strptime(response['birthday'], "%m/%d/%Y").strftime("%Y-%m-%d"),
                        password=get_random_string(length=32)
                    )
                return user

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None
