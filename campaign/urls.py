from django.conf.urls import url

from campaign.views import (
    CampaignListCreateView,
    CampaignRetrieveUpdateDestroyView,
    TwibbonListCreateView,
    TwibbonRetrieveUpdateDestroyView
)

urlpatterns = [
    url(r'^$',
        CampaignListCreateView.as_view(),
        name="campaign-list-create"),

    url(r'^(?P<campaign_url>[-\w]+)/$',
        CampaignRetrieveUpdateDestroyView.as_view(),
        name="campaign-retrieve-update-destroy"),

    url(r'^(?P<campaign_url>[-\w]+)/twibbons/$',
        TwibbonListCreateView.as_view(),
        name="twibbon-list-create"),

    url(r'^(?P<campaign_url>[-\w]+)/twibbons/(?P<twibbon_id>\d+)/$',
        TwibbonRetrieveUpdateDestroyView.as_view(),
        name="twibbon-retrieve-update-destroy"),
]
