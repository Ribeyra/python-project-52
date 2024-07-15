from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.get_full_name()
