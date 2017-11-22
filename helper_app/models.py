from django.db import models
from uuid import uuid4


def temporary_image_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    return "temp/{0}.{1}".format(uuid4().hex, ext)


class TemporaryImage(models.Model):
    img = models.ImageField(upload_to=temporary_image_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
