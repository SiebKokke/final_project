from django.urls import path
from .views import ArticleListAPI, PublisherListAPI, JournalistListAPI

urlpatterns = [
    path("articles/", ArticleListAPI.as_view(), name="api-article-list"),
    path("publishers/", PublisherListAPI.as_view(), name="api-publisher-list"),
    path(
        "journalists/",
        JournalistListAPI.as_view(),
        name="api-journalist-list",
    ),
]
