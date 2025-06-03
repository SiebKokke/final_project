from django.urls import path
from .views import (
    ArticleListView, ArticleDetailView,
    ArticleCreateView, ArticleUpdateView, ArticleDeleteView,
    approve_article,
    NewsletterListView,
    NewsletterDetailView,
    NewsletterCreateView,
    NewsletterUpdateView,
    NewsletterDeleteView,
    send_newsletter,
)

urlpatterns = [
    path("", ArticleListView.as_view(), name="article-list"),
    path(
        "article/<int:pk>/",
        ArticleDetailView.as_view(),
        name="article-detail",
    ),
    path("article/new/", ArticleCreateView.as_view(), name="article-create"),
    path(
        "article/<int:pk>/edit/",
        ArticleUpdateView.as_view(),
        name="article-edit",
    ),
    path(
        "article/<int:pk>/delete/",
        ArticleDeleteView.as_view(),
        name="article-delete",
    ),
    path("newsletters/", NewsletterListView.as_view(), name="newsletter-list"),
    path(
        "newsletters/new/",
        NewsletterCreateView.as_view(),
        name="newsletter-create",
    ),
    path(
        "newsletters/<int:pk>/",
        NewsletterDetailView.as_view(),
        name="newsletter-detail",
    ),
    path(
        "newsletters/<int:pk>/edit/",
        NewsletterUpdateView.as_view(),
        name="newsletter-edit",
    ),
    path(
        "newsletters/<int:pk>/delete/",
        NewsletterDeleteView.as_view(),
        name="newsletter-delete",
    ),
    path(
        "newsletters/<int:pk>/send/",
        send_newsletter,
        name="newsletter-send",
    ),
]
urlpatterns += [
    path("article/<int:pk>/approve/", approve_article, name="article-approve"),
]
