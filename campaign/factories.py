from factory import DjangoModelFactory, SubFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from utils.sample_images.getter import get_sample_image_file_path

from campaign.models import Campaign, Twibbon
from user.factories import UserFactory


class CampaignFactory(DjangoModelFactory):
    class Meta:
        model = Campaign

    name = "name"
    campaign_url = "asdfurl"
    twibbon_img = SimpleUploadedFile(
        name='jajaja.png',
        content=open(get_sample_image_file_path('1x1.png'), 'rb').read()
    )

    user = SubFactory(UserFactory)


class TwibbonFactory(DjangoModelFactory):
    class Meta:
        model = Twibbon

    user = SubFactory(UserFactory)
    campaign = SubFactory(CampaignFactory)
    img = SimpleUploadedFile(
        name='jajaja.png',
        content=open(get_sample_image_file_path('1x1.png'), 'rb').read()
    )
