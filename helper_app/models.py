from django.db import models
from uuid import uuid4


def temporary_image_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    return "temp/{0}.{1}".format(uuid4().hex, ext)

class TemporaryImage(models.Model):
    img = models.ImageField(upload_to=temporary_image_directory_path, height_field='height', width_field='width')
    relative_img = models.CharField(blank=True, null=True, max_length=500)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def scale(self):
        scalew = 1024.0/self.width
        scaleh = 1024.0/self.height
        return min(scalew,scaleh)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # TODO TEMPORARY FIX, FIND A BETTER WAY #
        tmp = TemporaryImage.objects.get(id=self.id)
        if(tmp.relative_img == None or tmp.relative_img == ''):
            tmp.relative_img = str(self.img)
            self.relative_img = str(self.img)
            tmp.save()



