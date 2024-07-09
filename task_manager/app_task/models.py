from django.db import models
from django.utils import timezone
from task_manager.app_status.models import Status
from task_manager.app_user.models import User
from task_manager.app_tag.models import Tag


class Task(models.Model):
    title = models.CharField(max_length=40, unique=True)
    description = models.TextField(blank=True, null=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name='tasks',
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='assigned_tasks',
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='task_tags'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name='created_tasks'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
