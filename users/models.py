from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    username = models.CharField(max_length=20)
    email = models.EmailField(_('email address'), unique=True)
    profile_image_url = models.TextField()
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
