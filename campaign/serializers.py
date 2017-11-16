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
            'created_at': {'read_only': True},
            'twibbon_img': {'required': True},
        }
