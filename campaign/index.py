from algoliasearch_django import AlgoliaIndex
from django.conf import settings

INDEX_NAME = 'prod_campaigns' if settings.PRODUCTION else 'dev_campaigns'

class CampaignIndex(AlgoliaIndex):
    fields = ('name', 'campaign_url', 'description', 'caption_template',
        'category', 'header_img', 'twibbon_img', 'city', 'started_at', 'finished_at', 'user')
    geo_field = 'location'
    settings = {'searchableAttributes': ['name', 'category', 'city', 'started_at', 'finished_at', 'user']}
    index_name = INDEX_NAME