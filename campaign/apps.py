from django.apps import AppConfig
import algoliasearch_django as algoliasearch

class CampaignConfig(AppConfig):
    name = 'campaign'

    def ready(self):
        YourModel = self.get_model('Campaign')
        algoliasearch.register(YourModel)