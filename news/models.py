from django.db import models
from users.models import CustomUser
from publishers.models import Publisher
# Create your models here.


class Article(models.Model):
    """Represents a news article submitted by a journalist."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    approved = models.BooleanField(default=False)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="articles"
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    """Represents a newsletter authored by a journalist or publisher."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="newsletters"
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="newsletters"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
