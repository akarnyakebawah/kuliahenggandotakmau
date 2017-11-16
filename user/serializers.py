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

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.date_joined = validated_data.get('date_joined', instance.date_joined)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.save()
        return instance
