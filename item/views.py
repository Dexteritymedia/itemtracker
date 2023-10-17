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

import pandas as pd
import plotly.express as px
from plotly.offline import plot

from .models import Item, ItemTracker, ItemDay
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
        items = ItemTracker.objects.filter(user=request.user).all().order_by('-modified_on')
        no_of_items = items.count()
        print(no_of_items)
        context = {'items': items, 'no_of_items': no_of_items}
        return render(request, 'home.html', context)
    else:
        context = {}
        return render(request, 'home.html', context)

def all_items(request):
    if request.user.is_authenticated:
        items = Item.objects.filter(user=request.user).all().order_by('item')
        no_of_items = items.count()
        df = pd.DataFrame(list(Item.objects.all().values()))
        dataframe = pd.DataFrame(list(Item.objects.filter(user=request.user).all().values('item',)))
        print(no_of_items)
        print(df)
        print(dataframe)
        context = {'items': items, 'no_of_items': no_of_items}
        return render(request, 'items_list.html', context)
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
            return redirect('items')
    else:
        form = ItemForm()
        context = {'form': form}
    return render(request, 'items.html', context)


def delete_item(request, item_id):
    query = Item.objects.get(id=item_id)
    if query.user != request.user:
        return Http404
    query.delete()
    return HttpResponse("Deleted!")

@login_required(login_url='user-login')
#@allowed_users(allowed_roles=['Admin'])
def item_edit(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('items')
    else:
        form = ItemForm(instance=item)
    context = {
        'form': form,
    }
    return render(request, 'items_edit.html', context)

@login_required(login_url='user-login')
def item_details(request, pk):
    item = get_object_or_404(Item, id=pk)
    if item.user != request.user:
        return Http404
    print(item.item)
    items = ItemTracker.objects.filter(user=request.user, item__item=item.item).all()
    print(items)
    if items:
        
        x = items.values_list('modified_on', flat=True)
        #x = items.values_list('modified_on__day', flat=True)#Use this to track the day, change day to second, minute, hour, week, or month, or year
        y = items.values_list('price', flat=True)
        fig = px.line(x=x, y=y, title=f"Breakdown of hoe much you spent on {item.item.title()}")
        fig.update_layout(
            xaxis_title="Date", yaxis_title="Price"
        )
        plot_div = plot(fig, show_link=False, output_type="div")
        context = {
            'item': item,
            'items': items,
            'plot_div': plot_div,
        }
    else:
        context = {
            'item': item,
            'items': items,
        }
        
    return render(request, 'items_details.html', context)

#Tracker Views
def list_item_tracker(request):
    if request.user.is_authenticated:
        tracker = ItemTracker.objects.filter(user=request.user).all().order_by('-modified_on')
        no_of_items = tracker.count()
        #item = ItemDay.objects.filter(user=request.user).all()
        #item_tracker = item.item_day_set.order_by('-modified_on')
        #print(item_tracker)
        #print(item)
        print(no_of_items)
        context = {'tracker': tracker, 'no_of_items': no_of_items}
        return render(request, 'tracker.html', context)
    else:
        context = {}
        return render(request, 'home.html', context)


@login_required(login_url="login")
def add_item_tracker(request):
    day = ItemDay.objects.get_or_create(date=timezone.now())
    #print(day)
    if request.method == 'POST':
        form = ItemTrackerForm(data=request.POST)
        if form.is_valid():
            new_item_tracker = form.save(commit=False)
            new_item_tracker.user = request.user
            new_item_tracker.item_day.date = day
            new_item_tracker.save()
            return redirect('home')
    else:
        form = ItemTrackerForm()
        context = {'form': form}
    return render(request, 'item_tracker.html', context)

"""
@login_required(login_url="login")
def item_tracker(request, item_id):
    item = ItemDayForm.objects.create(date=timezone.now())
    item_tracker = get_object_or_404(item, id=item_id)
    if item_tracker.user != request.user:
        return Http404
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
"""
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
