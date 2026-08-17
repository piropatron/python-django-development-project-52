from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.models import TimestampedModel


class Status(TimestampedModel):
    """Status of a task."""
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        unique=True,
        verbose_name=_('Name')
    )

    class Meta:
        verbose_name = _('Status')
        verbose_name_plural = _('Statuses')

    def __str__(self):
        return self.name
