from django.conf.urls import url

from campaign.views import CampaignListCreateView, CampaignUpdateDestroyView, TwibbonListCreateView, TwibbonUpdateDestroyView

urlpatterns = [
    url(r'^(?P<campaign_url>[-\w]+)/$',
        CampaignUpdateDestroyView.as_view(),
        name="campaign-update-destroy"),

    url(r'^$', CampaignListCreateView.as_view(), name="campaign-list-create"),

    url(r'^(?P<campaign_url>[-\w]+)/twibbons/(?P<twibbon_id>\d+)/$',
        TwibbonUpdateDestroyView.as_view(),
        name="campaign-update-destroy"),

    url(r'^(?P<campaign_url>[-\w]+)/twibbons/$', TwibbonListCreateView.as_view(), name="campaign-list-create"),
]
