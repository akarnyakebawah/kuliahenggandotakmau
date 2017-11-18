from rest_framework import serializers
from campaign.models import Campaign, Twibbon

from PIL import Image


def is_ratio_1x1(image):
    img = Image.open(image)
    width, height = img.size
    if width != height:
        raise serializers.ValidationError("image ratio must be 1:1")
    return image


class TwibbonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Twibbon
        fields = ('__all__')

        extra_kwargs = {
            'user': {'read_only': True}
        }

    def validate_img(self, value):
        return is_ratio_1x1(value)

    def create(self, validated_data):
        return Twibbon.objects.create(user=self.context['user'],
                                      **validated_data)


class CampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = ('__all__')

        extra_kwargs = {
            'created_at': {'read_only': True},
            'twibbon_img': {'required': True},
            'user': {'read_only': True},
        }

    def validate_twibbon_img(self, value):
        return is_ratio_1x1(value)

    def validate_campaign_url(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("url must be alhpanumeric")
        return value

    def create(self, validated_data):
        return Campaign.objects.create(user=self.context['user'],
                                       **validated_data)
