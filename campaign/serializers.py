from rest_framework import serializers
from campaign.models import Campaign, Twibbon


class TwibbonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Twibbon
        fields = ('__all__')

        extra_kwargs = {
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        return Twibbon.objects.create(user=self.context['user'],
                                      **validated_data)


class CampaignSerializer(serializers.ModelSerializer):

    twibbons = TwibbonSerializer(many=True, read_only=True)

    class Meta:
        model = Campaign
        fields = ('__all__')

        extra_kwargs = {
            'created_at': {'read_only': True},
            'twibbon_img': {'required': True},
            'user': {'read_only': True},
        }

    def create(self, validated_data):
        return Campaign.objects.create(user=self.context['user'],
                                       **validated_data)
