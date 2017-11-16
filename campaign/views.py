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
            'user': self.request.user,
        }


class CampaignUpdateDestroyView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsOwnerOrAdminOrReadOnly,)
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

    lookup_url_kwarg = 'campaign_url'

    def get_serializer_context(self):
        return {
            'user': self.request.user,
        }


class TwibbonListCreateView(generics.ListCreateAPIView):
    serializer_class = TwibbonSerializer

    def get_queryset(self):
        return Twibbon.objects.filter(campaign__slug=self.kwargs['campaign_url'])

    def get_serializer_context(self):
        return {
            'user': self.request.user,
        }


class TwibbonUpdateDestroyView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsOwnerOrAdminOrReadOnly,)
    serializer_class = TwibbonSerializer
    lookup_url_kwarg = 'twibbon_id'

    def get_queryset(self):
        return Twibbon.objects.filter(campaign__slug=self.kwargs['campaign_url'])

    def get_serializer_context(self):
        return {
            'user': self.request.user,
        }