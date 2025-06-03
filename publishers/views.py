from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from publishers.models import Publisher
# Create your views here.


class PublisherListView(ListView):
    """Displays a list of all publishers."""
    model = Publisher
    template_name = "publishers/publisher_list.html"
    context_object_name = "publishers"


class PublisherDetailView(DetailView):
    """Displays details for a single publisher."""
    model = Publisher
    template_name = "publishers/publisher_detail.html"
    context_object_name = "publisher"


class PublisherCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Allows editors or superusers to create a new publisher."""
    model = Publisher
    fields = ["name", "description", "editors", "journalists"]
    template_name = "publishers/publisher_form.html"
    success_url = reverse_lazy("publisher-list")

    def test_func(self):
        return (
            self.request.user.role == "editor" or
            self.request.user.is_superuser
        )


class PublisherUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows editors or superusers to update an existing publisher."""
    model = Publisher
    fields = ["name", "description", "editors", "journalists"]
    template_name = "publishers/publisher_form.html"
    success_url = reverse_lazy("publisher-list")

    def test_func(self):
        return (
            self.request.user.role == "editor" or
            self.request.user.is_superuser
        )
