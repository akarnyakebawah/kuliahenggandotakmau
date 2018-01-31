from utils.shortcuts import get_user_or_none
from rest_framework import generics
from campaign.models import Campaign, Twibbon
from campaign.permissions import IsOwnerOrAdminOrReadOnly
from campaign.serializers import CampaignSerializer, TwibbonSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CampaignListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

    def get_serializer_context(self):
        return {
            'user': get_user_or_none(self.request.user),
        }


class CampaignRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly,)
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

    lookup_url_kwarg = 'campaign_url'

    def get_serializer_context(self):
        return {
            'user': get_user_or_none(self.request.user),
        }


class TwibbonListCreateView(generics.ListCreateAPIView):
    serializer_class = TwibbonSerializer

    def get_queryset(self):
        return Twibbon.objects.filter(
            campaign__campaign_url=self.kwargs['campaign_url']
        )

    def get_serializer_context(self):
        return {
            'user': get_user_or_none(self.request.user),
            'campaign': Campaign.objects.get(campaign_url=self.kwargs['campaign_url'])
        }


class TwibbonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly,)
    serializer_class = TwibbonSerializer
    lookup_url_kwarg = 'twibbon_id'

    def get_queryset(self):
        return Twibbon.objects.filter(
            campaign__campaign_url=self.kwargs['campaign_url']
        )

    def get_serializer_context(self):
        return {
            'user': get_user_or_none(self.request.user),
            'campaign': Campaign.objects.get(campaign_url=self.kwargs['campaign_url'])
        }
