from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse
from .models import Article
from news.utils import post_to_twitter


@receiver(post_save, sender=Article)
def notify_subscribers_on_approval(sender, instance, created, **kwargs):
    """
    Send email to subscribers when an article is approved by an editor.
    """
    if not created and instance.approved:
        publisher = instance.publisher
        journalist = instance.author

        publisher_subs = (
            publisher.subscribed_readers.all()
            if publisher
            else []
        )
        journalist_subs = journalist.subscribed_by.all()

        all_subscribers = set(publisher_subs) | set(journalist_subs)
        all_emails = [user.email for user in all_subscribers if user.email]

        if all_emails:
            subject = f"New Article Approved: {instance.title}"
            message = (
                f"Dear subscriber,\n\n"
                f"A new article has been approved and published:\n\n"
                f"Title: {instance.title}\n"
                f"Author: {journalist.username}\n"
                f"Publisher: "
                f"{publisher.name if publisher else 'Independent'}\n\n"
                f"Read it here: http://127.0.0.1:8000"
                f"{reverse('article-detail', args=[instance.pk])}\n\n"
                f"Thank you for subscribing!"
            )
            send_mail(
                subject,
                message,
                None,
                all_emails,
                fail_silently=False,
            )
        """Post to Twitter when an article is approved."""
        status = (
            f"New article: {instance.title} by {journalist.username}. "
            f"Read it here: http://127.0.0.1:8000"
            f"{reverse('article-detail', args=[instance.pk])}"
        )
        post_to_twitter(status)
