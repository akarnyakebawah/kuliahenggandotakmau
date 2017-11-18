import os
from django.conf import settings


def get_sample_image_file_path(file_name):
        return os.path.join(settings.BASE_DIR, 'utils',
                            'sample_images', file_name)
