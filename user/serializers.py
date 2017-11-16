from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'birth_date', 'email', 'password')

        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'required': True},
            'email': {'required': True},
            'password': {'write_only': True},
            'birth_date': {'required': True},
        }
