from django.urls import path
from .views import (
    PublisherListView,
    PublisherDetailView,
    PublisherCreateView,
    PublisherUpdateView,
)

urlpatterns = [
    path("", PublisherListView.as_view(), name="publisher-list"),
    path("<int:pk>/", PublisherDetailView.as_view(), name="publisher-detail"),
    path("new/", PublisherCreateView.as_view(), name="publisher-create"),
    path(
        "<int:pk>/edit/",
        PublisherUpdateView.as_view(),
        name="publisher-edit",
    ),
]
