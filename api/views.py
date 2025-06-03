from django.shortcuts import render
from rest_framework import generics
from news.models import Article
from publishers.models import Publisher
from users.models import CustomUser
from .serializers import (
    ArticleSerializer,
    PublisherSerializer,
    JournalistSerializer,
)
# Create your views here.


class ArticleListAPI(generics.ListAPIView):
    """API view to list all approved articles."""
    queryset = Article.objects.filter(approved=True)
    serializer_class = ArticleSerializer


class PublisherListAPI(generics.ListAPIView):
    """API view to list all publishers."""
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class JournalistListAPI(generics.ListAPIView):
    """API view to list all journalists."""
    queryset = CustomUser.objects.filter(role="journalist")
    serializer_class = JournalistSerializer
