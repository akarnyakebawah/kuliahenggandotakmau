from django.db import models


class Campaign(models.Model):
    name = models.CharField(max_length=100)
    header_img = models.FileField()
    twibbon_img = models.FileField()


class Twibbon(models.Model):
    campaign = models.ForeignKey(Campaign, verbose_name="twibbons")
