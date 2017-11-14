from django.db import models
from user.models import User
from uuid import uuid4
from autoslug import AutoSlugField


def header_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    return "campaigns/{0}/{1}.{2}".format(instance.slug, "header", ext)


def twibbon_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    return "campaigns/{0}/{1}.{2}".format(instance.slug, "twibbon", ext)


# IMPORTANT!
# Tambahin tags
# Sebelum prod, hapus file migrations biar rapi
class Campaign(models.Model):
    name = models.CharField(max_length=100)
    hash_tag = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="name", unique=True, primary_key=True)

    description = models.TextField(blank=True)
    caption_template = models.TextField(blank=True)

    header_img = models.ImageField(upload_to=header_directory_path)
    twibbon_img = models.ImageField(upload_to=twibbon_directory_path)

    latitude = models.FloatField(blank=True, null=True)
    longtitude = models.FloatField(blank=True, null=True)
    city = models.CharField(max_length=100)

    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, related_name="campaigns",
                             on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.slug


def twibbon_item_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    return "campaigns/{0}/{1}.{2}".format(instance.campaign.slug, uuid4().hex, ext)


class Twibbon(models.Model):
    user = models.ForeignKey(User, related_name="twibbons",
                             on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, related_name="twibbons",
                                 on_delete=models.CASCADE)
    img = models.ImageField(upload_to=twibbon_item_directory_path)
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
