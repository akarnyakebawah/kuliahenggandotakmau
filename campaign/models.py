from django.db import models
from user.models import User
from uuid import uuid4


def header_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    return "campaigns/{0}/{1}.{2}".format(instance.campaign_url, "header", ext)


def twibbon_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    return "campaigns/{0}/{1}.{2}".format(instance.campaign_url, "twibbon", ext)


# IMPORTANT!
# Tambahin tags
# Sebelum prod, hapus file migrations biar rapi
class Campaign(models.Model):
    name = models.CharField(max_length=100)
    campaign_url = models.CharField(max_length=100, unique=True, primary_key=True)

    description = models.TextField(blank=True, null=True)
    caption_template = models.TextField(blank=True, null=True)

    header_img = models.ImageField(upload_to=header_directory_path, null=True, blank=True)
    twibbon_img = models.ImageField(upload_to=twibbon_directory_path)

    latitude = models.FloatField(blank=True, null=True)
    longtitude = models.FloatField(blank=True, null=True)
    city = models.CharField(blank=True, null=True, max_length=100)

    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, related_name="campaigns",
                             on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.campaign_url

    @property
    def owner_id(self):
        return self.user.id


def twibbon_item_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    return "campaigns/{0}/{1}.{2}".format(instance.campaign.campaign_url, uuid4().hex, ext)


class Twibbon(models.Model):
    user = models.ForeignKey(User, related_name="twibbons",
                             on_delete=models.CASCADE, null=True)
    campaign = models.ForeignKey(Campaign, related_name="twibbons",
                                 on_delete=models.CASCADE)
    img = models.ImageField(upload_to=twibbon_item_directory_path)
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def owner_id(self):
        if self.user:
            return self.user.id
        return -1
