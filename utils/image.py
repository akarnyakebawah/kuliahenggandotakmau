from rest_framework import serializers
from PIL import Image


def is_ratio_1x1(image):
    img = Image.open(image)
    width, height = img.size
    if width != height:
        raise serializers.ValidationError("image ratio must be 1:1")
    return image


def is_size_small(image):
    limit = 8 * 1024 * 1024  # 8 MiB
    if image.size > limit:
        raise serializers.ValidationError("Image too large. Size should not exceed 8 MiB")
    return image
