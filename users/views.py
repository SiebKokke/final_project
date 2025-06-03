from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from publishers.models import Publisher
from django.contrib.auth import login
from django.views.generic import ListView, DetailView
from .models import CustomUser

# Create your views here.


def signup(request):
    """Handle user signup."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("article-list")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def subscribe_publisher(request, pk):
    """Subscribe the logged-in user to a publisher."""
    publisher = get_object_or_404(Publisher, pk=pk)
    if request.user.role == "reader":
        request.user.subscriptions_publishers.add(publisher)
    return redirect("publisher-detail", pk=pk)


@login_required
def unsubscribe_publisher(request, pk):
    """Unsubscribe the logged-in user from a publisher."""
    publisher = get_object_or_404(Publisher, pk=pk)
    if request.user.role == "reader":
        request.user.subscriptions_publishers.remove(publisher)
    return redirect("publisher-detail", pk=pk)


# For journalists and subscribing to them

class JournalistListView(ListView):
    """List all journalists."""
    model = CustomUser
    template_name = "users/journalist_list.html"
    context_object_name = "journalists"

    def get_queryset(self):
        return CustomUser.objects.filter(role="journalist")


class JournalistDetailView(DetailView):
    """Detail view for a journalist."""
    model = CustomUser
    template_name = "users/journalist_detail.html"
    context_object_name = "journalist"


@login_required
def subscribe_journalist(request, pk):
    """Subscribe the logged-in user to a journalist."""
    journalist = get_object_or_404(CustomUser, pk=pk, role="journalist")
    request.user.subscriptions_journalists.add(journalist)
    return redirect("journalist-detail", pk=pk)


@login_required
def unsubscribe_journalist(request, pk):
    """Unsubscribe the logged-in user from a journalist."""
    journalist = get_object_or_404(CustomUser, pk=pk, role="journalist")
    request.user.subscriptions_journalists.remove(journalist)
    return redirect("journalist-detail", pk=pk)
