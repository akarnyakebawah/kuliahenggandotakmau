from django.apps import AppConfig
import algoliasearch_django as algoliasearch
from campaign.index import CampaignIndex

class CampaignConfig(AppConfig):
    name = 'campaign'

    def ready(self):
        model = self.get_model('Campaign')
        algoliasearch.register(model, CampaignIndex)
