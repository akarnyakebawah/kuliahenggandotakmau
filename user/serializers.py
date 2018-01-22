from rest_framework import serializers
from rest_framework_jwt.compat import PasswordField
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    password = PasswordField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'picture', 'birth_date', 'email', 'password')

        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'required': True},
            'username': {'required': True},
            'email': {'required': True},
            'birth_date': {'required': True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.save()
        return instance
