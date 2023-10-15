from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.HomeTemplateView.as_view(), name='home'),
    path("sign-up/", views.RegisterView.as_view(), name='register'),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("add-item/", views.add_item, name="add_item"),
    path("items/", views.all_items, name="items"),
    path("delete-item/<int:item_id>/", views.delete_item, name='delete-item'),
    path("edit-item/<int:pk>/", views.item_edit, name='edit-item'),
    path("list-all-tracked-items/", views.list_item_tracker, name='tracker'),
    #path("track-item/", views.item_tracker, name="tracker"),
]
    
