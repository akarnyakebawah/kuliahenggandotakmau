from rest_framework import serializers
from campaign.models import Campaign, Twibbon, Category
from utils.image import is_ratio_1x1, is_size_small


class TwibbonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Twibbon
        fields = ('__all__')

        extra_kwargs = {
            'user': {'read_only': True},
            'campaign': {'read_only': True}
        }

    def validate_img(self, value):
        return is_ratio_1x1(value) and is_size_small(value)

    def create(self, validated_data):
        return Twibbon.objects.create(
            user=self.context.get('user'),
            campaign=self.context.get('campaign'),
            **validated_data
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'description', 'created_at')

        # assuming this model can only created from django admin
        extra_kwargs = {
            'name': {'read_only': True},
            'description': {'read_only': True},
            'created_at': {'read_only': True},
        }


class CampaignSerializer(serializers.ModelSerializer):

    twibbon_count = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = ('__all__')

        extra_kwargs = {
            'category': {'required': False},
            'created_at': {'read_only': True},
            'twibbon_img': {'required': True},
            'user': {'read_only': True},
        }

    def validate_twibbon_img(self, value):
        return is_ratio_1x1(value) and is_size_small(value)

    def validate_campaign_url(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("url must be alphanumeric")
        return value

    def create(self, validated_data):
        return Campaign.objects.create(
            user=self.context.get('user'),
            **validated_data
        )

    def get_twibbon_count(self, obj):
        return obj.twibbons.all().count()
