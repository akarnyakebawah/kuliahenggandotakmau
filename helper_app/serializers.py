from rest_framework import serializers
from helper_app.models import TemporaryImage
from utils.image import is_ratio_1x1, is_size_small


class TemporaryImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = TemporaryImage
        fields = ('img', 'relative_img', 'width', 'height', 'created_at', 'scale')

        extra_kwargs = {
            'created_at': {'read_only': True}
        }

    def validate_img(self, value):
        return is_size_small(value)
