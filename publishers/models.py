from django.db import models
from users.models import CustomUser
# Create your models here.


class Publisher(models.Model):
    """Represents a news publisher."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    editors = models.ManyToManyField(
        CustomUser, related_name="publisher_editors"
    )
    journalists = models.ManyToManyField(
        CustomUser, related_name="publisher_journalists"
    )

    def __str__(self):
        return self.name
