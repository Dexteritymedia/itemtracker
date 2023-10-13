from django.contrib import admin
from .models import ItemTracker, Item, ItemDay
# Register your models here.

admin.site.register(ItemTracker)
admin.site.register(Item)
admin.site.register(ItemDay)
