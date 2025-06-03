from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import Article, Newsletter


def setup_groups_permissions(sender, **kwargs):
    """
    Setup groups and permissions for the news application.

    This ensures both Article and Newsletter permissions are set for
    Reader, Editor, and Journalist groups.
    """
    try:
        # Article ContentType and Permissions
        article_ct = ContentType.objects.get_for_model(Article)
        can_add_article = Permission.objects.get(
            codename="add_article", content_type=article_ct
        )
        can_change_article = Permission.objects.get(
            codename="change_article", content_type=article_ct
        )
        can_delete_article = Permission.objects.get(
            codename="delete_article", content_type=article_ct
        )
        can_view_article = Permission.objects.get(
            codename="view_article", content_type=article_ct
        )

        # Newsletter ContentType and Permissions
        newsletter_ct = ContentType.objects.get_for_model(Newsletter)
        can_add_newsletter = Permission.objects.get(
            codename="add_newsletter", content_type=newsletter_ct
        )
        can_change_newsletter = Permission.objects.get(
            codename="change_newsletter", content_type=newsletter_ct
        )
        can_delete_newsletter = Permission.objects.get(
            codename="delete_newsletter", content_type=newsletter_ct
        )
        can_view_newsletter = Permission.objects.get(
            codename="view_newsletter", content_type=newsletter_ct
        )
    except Permission.DoesNotExist:
        # Permissions not ready yet; skip group setup for now
        return

    """Groups"""
    # Reader: Can view articles and newsletters
    reader_group, _ = Group.objects.get_or_create(name="Reader")
    reader_group.permissions.set([can_view_article, can_view_newsletter])

    # Editor: Can view, change, delete articles/newsletters (but not add)
    editor_group, _ = Group.objects.get_or_create(name="Editor")
    editor_group.permissions.set([
        can_view_article, can_change_article, can_delete_article,
        can_view_newsletter, can_change_newsletter, can_delete_newsletter
    ])

    # Journalist: Can add, view, change, delete articles/newsletters
    journalist_group, _ = Group.objects.get_or_create(name="Journalist")
    journalist_group.permissions.set([
        can_add_article,
        can_view_article,
        can_change_article,
        can_delete_article,
        can_add_newsletter,
        can_view_newsletter,
        can_change_newsletter,
        can_delete_newsletter
    ])


def ready_groups_permissions(sender, **kwargs):
    """
    Signal to setup groups and permissions post-migrate.
    """
    post_migrate.connect(setup_groups_permissions, sender=sender)
