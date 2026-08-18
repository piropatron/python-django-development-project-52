from django.db import models

from task_manager.models import TimestampedModel


# Create your models here.
class Tag(TimestampedModel, models.Model):
    """A tag for the group of posts."""

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name