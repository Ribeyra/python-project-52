from django.contrib.auth.models import AbstractUser
from django.db import models    # noqa f401


class User(AbstractUser):
    def __str__(self):
        return self.get_full_name()
