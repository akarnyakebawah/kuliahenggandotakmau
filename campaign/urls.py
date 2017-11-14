from django.conf.urls import url

from campaign.views import CampaignListCreateView, CampaignUpdateDestoryView, TwibbonListCreateView, TwibbonUpdateDestoryView

urlpatterns = [
    url(r'^(?P<campaign_slug>[-\w]+)/$',
        CampaignUpdateDestoryView.as_view(),
        name="campaign-update-destroy"),

    url(r'^$', CampaignListCreateView.as_view(), name="campaign-list-create"),

    url(r'^(?P<campaign_slug>[-\w]+)/twibbons/(?P<twibbon_id>\d+)/$',
        TwibbonUpdateDestoryView.as_view(),
        name="campaign-update-destroy"),

    url(r'^(?P<campaign_slug>[-\w]+)/twibbons/$', TwibbonListCreateView.as_view(), name="campaign-list-create"),
]
