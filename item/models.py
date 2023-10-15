from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
# Create your models here.


User = get_user_model()


class ItemDay(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    note = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
            
    def __str__(self):
        if self.user == None:
            return None
        return f"Created by {self.user.username} on {self.date}"

    class Meta:
        #the day on which a tracker is created would be sorted in reverse order Z-A
        ordering = ["-date"]
        verbose_name = "Item"
        verbose_name_plural = "Item"
		
class Item(models.Model):
    ITEM_TYPE = (
        ("service", "Service"),
        ("goods", "Goods"),
    )
	
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    item = models.CharField(max_length=50, blank=False)
    item_type = models.CharField(choices=ITEM_TYPE, max_length=50, default="service", null=True, blank=True)
	
    def __str__(self):
        if self.user == None:
            return f"{self.item}"
        return f"{self.item} added by {self.user.username}"
	
    class Meta:
        #the items would be sorted alphabetically in reverse order Z-A
        ordering = ["-item"]
        verbose_name = "Item"
        verbose_name_plural = "Items"

        
class ItemTracker(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_day = models.ForeignKey(ItemDay, on_delete=models.CASCADE, related_name='item')
    price = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    debt = models.BooleanField(default=False, verbose_name="Credit/Debit", help_text="Click the box if purchase is on credit")
	
    def __str__(self):
        return f"""
                Added {self.item} on {self.created_on}, modified {self.modified_on}, Debt {self.debt}"""

    @property
    def schedules(self):
        return self.item_day_set.all().order_by('modified_on')
		
    @property
    def debt_purchased(self):
        if self.debt == True:
            return -(self.price)
		
