from core.utils import avatar_upload
from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    GENDER_CHOICES = (('Male', 'Male'),('Female', 'Female'))

    gender = models.CharField(max_length=6, blank=True, choices=GENDER_CHOICES)
    avatar = models.ImageField(upload_to=avatar_upload, default='avatars/default.png')


    def __str__(self):
        return self.username
