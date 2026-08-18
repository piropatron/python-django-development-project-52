from django.db import models

from task_manager.models import TimestampedModel

from django.utils.translation import gettext_lazy as _



# Create your models here.
class Label(TimestampedModel, models.Model):
    """A tag for the group of posts."""

    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        unique=True,
        verbose_name=_('Name')
    )

    def __str__(self):
        return self.name