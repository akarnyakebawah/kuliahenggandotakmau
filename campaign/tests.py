# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse

from rest_framework.test import APITestCase

from user.factories import UserFactory
from campaign.factories import CampaignFactory, TwibbonFactory
from campaign.models import Campaign, Twibbon
from utils.sample_images.getter import get_sample_image_file_path


class CampaignTests(APITestCase):

    def test_owner_id(self):
        user = UserFactory()
        campaign = CampaignFactory(user=user)
        self.assertEqual(user.id, campaign.owner_id)

    def test_get_list_campaigns_success(self):
        CampaignFactory.create(name="campaign1")
        response = self.client.get(reverse('campaign-list-create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]["name"], "campaign1")

    def test_post_campaign_success(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.post(reverse('campaign-list-create'), {
            'name': 'Nama',
            'campaign_url': 'url',
            'twibbon_img': open(get_sample_image_file_path('1x1.png'), 'rb')
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Campaign.objects.all().count(), 1)
        self.assertEqual(Campaign.objects.first().name, 'Nama')

    def test_post_campaign_without_user(self):
        response = self.client.post(reverse('campaign-list-create'), {
            'name': 'Nama',
            'campaign_url': 'url',
            'twibbon_img': open(get_sample_image_file_path('1x1.png'), 'rb')
        })
        self.assertEqual(response.status_code, 401)

    def test_post_campaign_with_2x1_image(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.post(reverse('campaign-list-create'), {
            'name': 'Nama',
            'campaign_url': 'url',
            'twibbon_img': open(get_sample_image_file_path('2x1.png'), 'rb')
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['twibbon_img'], ['image ratio must be 1:1'])

    def test_post_campaign_with_invalid_campaign_url(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.post(reverse('campaign-list-create'), {
            'name': 'Nama',
            'campaign_url': 'url!',
            'twibbon_img': open(get_sample_image_file_path('1x1.png'), 'rb')
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['campaign_url'], ["url must be alphanumeric"])

    def test_post_campaign_owner_is_valid(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        self.client.post(reverse('campaign-list-create'), {
            'name': 'Nama',
            'campaign_url': 'url',
            'twibbon_img': open(get_sample_image_file_path('1x1.png'), 'rb')
        })
        campaign = Campaign.objects.first()
        self.assertEqual(campaign.owner_id, user.id)

    def test_put_campaign_success(self):
        campaign = CampaignFactory(name="campaign1")
        self.client.force_authenticate(user=campaign.user)
        response = self.client.put(
            reverse(
                'campaign-retrieve-update-destroy',
                kwargs={'campaign_url': campaign.campaign_url}),
            {'name': 'Nama',
             'campaign_url': 'url',
             'twibbon_img': open(get_sample_image_file_path('1x1.png'), 'rb')}
        )
        new_campaign = Campaign.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_campaign.name, 'Nama')

    def test_put_campaign_user_unauthorized(self):
        campaign = CampaignFactory(name="campaign1")
        response = self.client.put(
            reverse(
                'campaign-retrieve-update-destroy',
                kwargs={'campaign_url': campaign.campaign_url}),
            {'name': 'Nama',
             'campaign_url': 'url',
             'twibbon_img': open(get_sample_image_file_path('1x1.png'), 'rb')}
        )
        self.assertEqual(response.status_code, 401)

    def test_put_campaign_user_forbidden(self):
        user1 = UserFactory(email="email1@email.email")
        user2 = UserFactory(email="email2@email.emaul")
        campaign = CampaignFactory(name="campaign1", user=user1)
        self.client.force_authenticate(user=user2)
        response = self.client.put(
            reverse(
                'campaign-retrieve-update-destroy',
                kwargs={'campaign_url': campaign.campaign_url}),
            {'name': 'Nama',
             'campaign_url': 'url',
             'twibbon_img': open(get_sample_image_file_path('1x1.png'), 'rb')}
        )
        self.assertEqual(response.status_code, 403)


class TwibbonTests(APITestCase):

    def test_owner_id(self):
        user = UserFactory(email="email1@email.email")
        twibbon = TwibbonFactory(user=user)
        self.assertEqual(twibbon.owner_id, user.id)

    def test_get_twibbons_success(self):
        user1 = UserFactory(email="user1@a.b")
        user2 = UserFactory(email="user2@a.b")
        campaign = CampaignFactory(user=user1)
        TwibbonFactory(campaign=campaign, user=user2, caption="caption")
        response = self.client.get(
            reverse(
                'twibbon-list-create',
                kwargs={'campaign_url': campaign.campaign_url})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['caption'], 'caption')
        self.assertEqual(response.data['results'][0]['user'], user2.id)

    def test_post_twibbon_success(self):
        user = UserFactory(email="user@asdfa.b")
        campaign1 = CampaignFactory(user=user)
        self.client.force_authenticate(user=user)
        response = self.client.post(
            reverse(
                'twibbon-list-create',
                kwargs={'campaign_url': campaign1.campaign_url}),
            {'img': open(get_sample_image_file_path('1x1.png'), 'rb')}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Twibbon.objects.all().count(), 1)
        self.assertEqual(campaign1.twibbons.all().count(), 1)

    def test_post_twibbon_without_user(self):
        user = UserFactory()
        campaign = CampaignFactory(user=user)
        response = self.client.post(
            reverse(
                'twibbon-list-create',
                kwargs={'campaign_url': campaign.campaign_url}),
            {'img': open(get_sample_image_file_path('1x1.png'), 'rb')}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Twibbon.objects.all().count(), 1)

    def test_post_twibbon_with_2x1_image(self):
        campaign = CampaignFactory()
        response = self.client.post(
            reverse(
                'twibbon-list-create',
                kwargs={'campaign_url': campaign.campaign_url}),
            {'img': open(get_sample_image_file_path('2x1.png'), 'rb')}
        )
        self.assertEqual(response.status_code, 400)
