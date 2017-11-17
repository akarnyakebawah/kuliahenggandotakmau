from rest_framework import generics
from user.models import User
from user.serializers import UserSerializer


class UserListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        if self.request.user:
            if self.request.user.is_superuser:
                return User.objects.all()
            return User.objects.filter(id=self.request.user.id)
        return []

    serializer_class = UserSerializer


class UserUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        if self.request.user:
            if self.request.user.is_superuser:
                return User.objects.all()
            return User.objects.filter(id=self.request.user.id)
        return []

    serializer_class = UserSerializer
    lookup_url_kwarg = 'user_id'
