from rest_framework import generics
from campaign.models import Campaign, Twibbon
from campaign.permissions import IsOwnerOrAdminOrReadOnly
from campaign.serializers import CampaignSerializer, TwibbonSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CampaignListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer


class CampaignUpdateDestoryView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsOwnerOrAdminOrReadOnly,)
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

    lookup_url_kwarg = 'campaign_slug'


class TwibbonListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        return Twibbon.objects.filter(campaign__slug=self.kwargs['campaign_slug'])
    serializer_class = TwibbonSerializer


class TwibbonUpdateDestoryView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsOwnerOrAdminOrReadOnly,)
    def get_queryset(self):
        return Twibbon.objects.filter(campaign__slug=self.kwargs['campaign_slug'])
    serializer_class = TwibbonSerializer
    lookup_url_kwarg = 'twibbon_id'
