from django.urls import path
from .views import (
    signup,
    subscribe_publisher,
    unsubscribe_publisher,
    JournalistListView,
    JournalistDetailView,
    subscribe_journalist,
    unsubscribe_journalist,
)

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("journalists/", JournalistListView.as_view(), name="journalist-list"),
    path(
        "journalists/<int:pk>/",
        JournalistDetailView.as_view(),
        name="journalist-detail",
    ),
    path(
        "subscribe/publisher/<int:pk>/",
        subscribe_publisher,
        name="subscribe-publisher",
    ),
    path(
        "unsubscribe/publisher/<int:pk>/",
        unsubscribe_publisher,
        name="unsubscribe-publisher",
    ),
    path(
        "subscribe/journalist/<int:pk>/",
        subscribe_journalist,
        name="subscribe-journalist",
    ),
    path(
        "unsubscribe/journalist/<int:pk>/",
        unsubscribe_journalist,
        name="unsubscribe-journalist",
    ),
]
