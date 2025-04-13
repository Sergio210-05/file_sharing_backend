import os

from django.contrib.auth.models import AbstractUser
from django.db import models

from file_sharing.settings import MEDIA_ROOT


class User(AbstractUser):
    full_name = models.CharField(max_length=100)
    password = models.CharField(max_length=250, unique=True)
    folder_path = models.CharField(max_length=250, default='', blank=True)

    REQUIRED_FIELDS = ["full_name", "email", "password", ]

    def save(self, *args, **kwargs):
        if not self.folder_path:
            user_folder = os.path.join(MEDIA_ROOT, self.username)
            os.makedirs(user_folder)
            self.folder_path = user_folder
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
