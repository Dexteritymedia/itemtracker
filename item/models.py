from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


User = get_user_model()


class ItemDay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
            
    def __str__(self):
        return f"Created by {self.user.username}"
		
class Item(models.Model):
    ITEM_TYPE = (
        ("service", "Service"),
        ("goods", "Goods"),
    )
	
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=50, blank=False)
    item_type = models.CharField(choices=ITEM_TYPE, max_length=50, default="service", null=True, blank=True)
	
    def __str__(self):
        return f"{self.item_type}"
	
    class Meta:
        #the students would be sorted alphabetically by last_name, from A-Z, and then by first_name and middle_name, in reverse order Z-A
        ordering = ["-item"]

        
class ItemTracker(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_day = models.ForeignKey(ItemDay, on_delete=models.CASCADE, related_name='item')
    price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    debt = models.BooleanField(default=False, verbose_name="Credit/Debit", help_text="Click the box if purchase is on credit")
	
    def __str__(self):
        return f"{self.item}, {self.debt}"
		
    @property
    def debt_purchased(self):
        if self.debt == True:
            return -(self.price)
		
