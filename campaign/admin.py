# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from campaign.models import Campaign, Twibbon
from django.contrib import admin


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'campaign_url', 'twibbon_img', 'city',
                    'started_at', 'finished_at', 'created_at', 'user')


@admin.register(Twibbon)
class TwibbonAdmin(admin.ModelAdmin):
    list_display = ('user', 'campaign', 'img', 'created_at')
