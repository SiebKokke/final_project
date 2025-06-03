from django.db import models
from django.contrib.auth.models import AbstractUser, Group
# Create your models here.


class CustomUser(AbstractUser):
    """Custom user model with role-based fields for the news app."""
    ROLE_CHOICES = (
        ("reader", "Reader"),
        ("editor", "Editor"),
        ("journalist", "Journalist"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    subscriptions_publishers = models.ManyToManyField(
        "publishers.Publisher", blank=True, related_name="subscribed_readers"
    )
    subscriptions_journalists = models.ManyToManyField(
        "self", blank=True, symmetrical=False, related_name="subscribed_by"
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.groups.clear()
        if self.role:
            try:
                group = Group.objects.get(name=self.role.capitalize())
                self.groups.add(group)
            except Group.DoesNotExist:
                pass
