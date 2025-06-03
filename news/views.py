from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Article, Newsletter
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied


class ArticleListView(LoginRequiredMixin, ListView):
    """
    Displays a list of all approved articles, or all articles for
    users with view permission.
    """
    model = Article
    template_name = "news/article_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.has_perm("news.view_article"):
            return Article.objects.all()
        return Article.objects.filter(approved=True)


class ArticleDetailView(
    LoginRequiredMixin, PermissionRequiredMixin, DetailView
):
    """Displays the details of a single article."""
    model = Article
    template_name = "news/article_detail.html"
    context_object_name = "article"
    permission_required = "news.view_article"


class ArticleCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateView
):
    """Allows users with add_article permission to create new articles."""
    model = Article
    fields = ["title", "content", "publisher"]
    template_name = "news/article_form.html"
    permission_required = "news.add_article"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("article-list")


class ArticleUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
    UpdateView,
):
    """
    Allows users with change_article permission to update articles.
    Editors can update any journalists can update their own.
    """
    model = Article
    fields = ["title", "content", "publisher", "approved"]
    template_name = "news/article_form.html"
    permission_required = "news.change_article"

    def test_func(self):
        article = self.get_object()
        user = self.request.user
        # Editors can edit any, journalists only their own
        return user.has_perm("news.change_article") and (
            user.groups.filter(name="Editor").exists() or
            article.author == user
        )

    def get_success_url(self):
        return reverse_lazy("article-list")


class ArticleDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):
    """
    Allows users with delete_article permission to delete articles.
    Editors can delete any journalists can delete their own.
    """
    model = Article
    template_name = "news/article_confirm_delete.html"
    permission_required = "news.delete_article"

    def test_func(self):
        article = self.get_object()
        user = self.request.user
        return user.has_perm("news.delete_article") and (
            user.groups.filter(name="Editor").exists() or
            article.author == user
        )

    def get_success_url(self):
        return reverse_lazy("article-list")


@login_required
@permission_required("news.change_article", raise_exception=True)
def approve_article(request, pk):
    """
    Allows users with change_article permission
    to approve a submitted article.
    """
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        article.approved = True
        article.save()
        return redirect(reverse("article-detail", args=[pk]))
    return redirect(reverse("article-detail", args=[pk]))


# Newsletters Views
class NewsletterListView(
    LoginRequiredMixin, PermissionRequiredMixin, ListView
):
    """Displays a list of newsletters."""
    model = Newsletter
    template_name = "news/newsletter_list.html"
    context_object_name = "newsletters"
    permission_required = "news.view_newsletter"


class NewsletterDetailView(
    LoginRequiredMixin, PermissionRequiredMixin, DetailView
):
    """Displays the details of a single newsletter."""
    model = Newsletter
    template_name = "news/newsletter_detail.html"
    context_object_name = "newsletter"
    permission_required = "news.view_newsletter"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        newsletter = self.get_object()
        # Editors can send any journalists only their own
        context["can_send_newsletter"] = (
            user.groups.filter(name="Editor").exists() or
            newsletter.author == user
        )
        return context


class NewsletterCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    """Allows users with add_newsletter permission to create newsletters."""
    model = Newsletter
    fields = ["title", "content", "publisher"]
    template_name = "news/newsletter_form.html"
    permission_required = "news.add_newsletter"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("newsletter-list")


class NewsletterUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
    UpdateView,
):
    """
    Allows users with change_newsletter permission to update newsletters.
    Editors can update any journalists only their own.
    """
    model = Newsletter
    fields = ["title", "content", "publisher"]
    template_name = "news/newsletter_form.html"
    permission_required = "news.change_newsletter"

    def test_func(self):
        newsletter = self.get_object()
        user = self.request.user
        return user.has_perm("news.change_newsletter") and (
            user.groups.filter(name="Editor").exists() or
            newsletter.author == user
        )

    def get_success_url(self):
        return reverse_lazy("newsletter-list")


class NewsletterDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):
    """
    Allows users with delete_newsletter permission to delete newsletters.
    Editors can delete any journalists only their own.
    """
    model = Newsletter
    template_name = "news/newsletter_confirm_delete.html"
    permission_required = "news.delete_newsletter"

    def test_func(self):
        newsletter = self.get_object()
        user = self.request.user
        return user.has_perm("news.delete_newsletter") and (
            user.groups.filter(name="Editor").exists() or
            newsletter.author == user
        )

    def get_success_url(self):
        return reverse_lazy("newsletter-list")


@login_required
@permission_required("news.change_newsletter", raise_exception=True)
def send_newsletter(request, pk):
    """
    Sends the newsletter to all subscribers.
    Editors can send any journalists only their own.
    """
    newsletter = get_object_or_404(Newsletter, pk=pk)
    user = request.user
    # Editors can send any, journalists only their own
    if not (
        user.groups.filter(name="Editor").exists() or newsletter.author == user
    ):
        raise PermissionDenied

    publisher = newsletter.publisher
    author = newsletter.author
    publisher_subs = publisher.subscribed_readers.all() if publisher else []
    journalist_subs = author.subscribed_by.all()
    all_subscribers = set(publisher_subs) | set(journalist_subs)
    all_emails = [u.email for u in all_subscribers if u.email]

    if request.method == "POST" and all_emails:
        subject = f"Newsletter: {newsletter.title}"
        message = (
            f"{newsletter.content}\n\n"
            f"From: {author.username} "
            f"({publisher.name if publisher else 'Independent'})"
        )
        send_mail(subject, message, None, all_emails, fail_silently=False)
        newsletter.sent_at = timezone.now()
        newsletter.save()
        return redirect("newsletter-detail", pk=newsletter.pk)
    return render(
        request,
        "news/send_newsletter_confirm.html",
        {"newsletter": newsletter},
    )
