from rest_framework import serializers
from helper_app.models import TemporaryImage


class TemporaryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryImage
        fields = ('__all__')

        extra_kwargs = {
            'created_at': {'read_only': True}
        }
