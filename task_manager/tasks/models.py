from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.models import TimestampedModel
from task_manager.statuses.models import Status


# Create your models here.
class Task(TimestampedModel, models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'), unique=True)
    description = models.TextField(verbose_name=_('Description'))
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name=_('Status'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks', verbose_name=_('Author'))
    executor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='my_tasks', verbose_name=_('Executor'))
    labels = models.ManyToManyField(Label, related_name='tasks')

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return self.name
