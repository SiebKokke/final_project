from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import Article, Newsletter


class Command(BaseCommand):
    """Initializes user groups and assigns relevant permissions."""

    def handle(self, *args, **kwargs):
        """Create user groups and assign permissions."""
        reader_group, created = Group.objects.get_or_create(name="Reader")
        journalist_group, created = Group.objects.get_or_create(
            name="Journalist"
        )
        editor_group, created = Group.objects.get_or_create(name="Editor")

        article_ct = ContentType.objects.get_for_model(Article)
        newsletter_ct = ContentType.objects.get_for_model(Newsletter)

        """Only reader can view articles and newsletters."""
        reader_perms = Permission.objects.filter(
            content_type__in=[article_ct, newsletter_ct],
            codename__startswith="view_"
        )
        reader_group.permissions.set(reader_perms)

        """Journalist can add, change, delete, view own"""
        journalist_perms = Permission.objects.filter(
            content_type__in=[article_ct, newsletter_ct],
            codename__startswith=("add_", "change_", "delete_", "view_")
        )
        journalist_group.permissions.set(journalist_perms)

        """Editor can do everything"""
        editor_perms = Permission.objects.filter(
            content_type__in=[article_ct, newsletter_ct],
        )
        editor_group.permissions.set(editor_perms)

        self.stdout.write(
            self.style.SUCCESS("Groups and permissions initialized.")
        )
