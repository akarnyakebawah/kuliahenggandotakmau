from rest_framework import serializers
from campaign.models import Campaign, Twibbon


class TwibbonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Twibbon
        fields = ('__all__')


class CampaignSerializer(serializers.ModelSerializer):

    twibbons = TwibbonSerializer(many=True, read_only=True)

    class Meta:
        model = Campaign
        fields = ('__all__')

        extra_kwargs = {
            'slug': {'read_only': True},
            'created_at': {'read_only': True},
            'header_img': {'required': True},
            'twibbon_img': {'required': True},
        }
