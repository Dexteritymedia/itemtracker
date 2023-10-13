from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView, View, FormView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone

#from .models import 
#from .utils import *
from .forms import SignUpForm, ItemDayForm, ItemTrackerForm, ItemForm

class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = SignUpForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)

        return super(RegisterView, self).form_valid(form)


def login_page(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f"Welcome {username}!!!")
            return redirect("home")
        else:
            messages.info(request, f"Account does not exist please sign up or check your account details")
    form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def logout_page(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")


class HomeTemplateView(TemplateView):
    template_name = "index.html"

def home(request):
    if request.user.is_authenticated:
        items = ItemTrackerForm.objects.filter(user=request.user).all().order_by('-date')
        context = {'items': items}
        return render(request, 'home.html', context)
    else:
        context = {}
        return render(request, 'home.html', context)


@login_required(login_url="login")
def add_item(request):
    """Add a new item"""
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            return redirect('home')
        else:
            form = ItemForm()
            context = {'form': form}
    return render(request, 'items.html', context)


@login_required(login_url="login")
def item_tracker(request):
    """Add a new session for a particular chat."""
    if request.method == 'POST':
        form = ItemTrackerForm(data=request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            return redirect('home')
        else:
            form = ItemTrackerForm()
            context = {'form': form}
    return render(request, 'item_tracker.html', context)


@login_required(login_url="login")
def item_tracker(request, item_id):
    item = ItemDayForm.objects.create(date=timezone.now())
    item_tracker = get_object_or_404(item, id=item_id)
    if item_tracker.user != request.user:
        return Http404
    """Add a new session for a particular chat."""
    if request.method == 'POST':
        form = ItemTrackerForm(data=request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            return redirect('home')
        else:
            form = ItemTrackerForm()
            context = {'form': form}
    return render(request, 'item_tracker.html', context)

@login_required(login_url="login")
def item_list(request, item_id):
    item = ItemDay.objects.get(id=item_id)
    item_tracker = item.item_set.order_by('-date_added')
    context = {'item': item, 'item_tracker': item_tracker}
    return render(request, '', context)

@login_required(login_url="login")
def item_list(request, item_id):
    item = get_object_or_404(ItemDay, id=item_id)
    item_tracker = ItemDay.objects.all().filter(item)
    context = {'item': item, 'item_tracker': item_tracker}
    return render(request, '', context)
