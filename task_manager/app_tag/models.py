from django.db import models
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
