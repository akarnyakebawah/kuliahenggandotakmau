from rest_framework import generics, status, views, response
from django.core.mail import EmailMessage
from user.models import User
from user.serializers import UserSerializer
from user.permissions import IsOwnerOrAdmin

from datetime import datetime, timedelta

from rest_framework_jwt.settings import api_settings

class UserListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        if self.request.user:
            if self.request.user.is_superuser:
                return User.objects.all()
            return User.objects.filter(id=self.request.user.id)
        return []

    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        if self.request.user:
            if self.request.user.is_superuser:
                return User.objects.all()
            return User.objects.filter(id=self.request.user.id)
        return []

    permission_classes = (IsOwnerOrAdmin,)
    serializer_class = UserSerializer
    lookup_url_kwarg = 'user_id'

class UserRequestPasswordResetView(views.APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            return response.Response(status=status.HTTP_404_NOT_FOUND)

        # TODO change to constant 
        hours_to_expired = 1

        # TODO don't compare with unix timestamp lol
        expired_date = (datetime.now() + timedelta(hours=hours_to_expired)).timestamp()
        print(expired_date)

        payload = {
            "email": user.email,
            "password": user.password,
            "expired_date": expired_date
        }

        token = api_settings.JWT_ENCODE_HANDLER(payload)
        email = EmailMessage(
            subject='Twiggsy.com Password Reset',
            body='''You recently requested a password reset for your Twiggsy.com Account.
To reset your password, use this token lol:\n''' + token + '''
Sincerely,
The Twiggsy Team''',
            to=[user.email]
        )
        email.send()

        return response.Response()

class UserConfirmPasswordResetView(views.APIView):
    def post(self, request, *args, **kwargs):
        try:
            payload = api_settings.JWT_DECODE_HANDLER(request.data['token'])
        except Exception:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=payload['email'])

        ## TODO same as above, don't compare with unix timestamp
        if(payload['password'] != user.password or payload['expired_date'] <= datetime.now().timestamp()):
            ## TODO probably change http code
            return response.Response(status=status.HTTP_400_BAD_REQUEST)

        password_new = request.data['password']
        user.set_password(password_new)
        user.save()
        return response.Response()


