import os
import uuid
from django.db import models


class CuisineManager(models.Manager):

    def recipe_image_file_path(instance, filename):
        """Generates file path for new recipe image"""
        extension = filename.split('.')[-1]
        filename = f'{uuid.uuid4()}.{extension}'

        return os.path.join('uploads/recipe/', filename)
