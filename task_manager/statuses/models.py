from cProfile import label

from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class TimestampedModel(models.Model):
    """An abstract model with a pair of timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Status(TimestampedModel):
    """Status of a task."""
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        unique=True,
        verbose_name=_('Name')
    )
