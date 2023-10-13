from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import ItemDay, Item, ItemTracker 

User = get_user_model()

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Enter your first name')
    last_name = forms.CharField(max_length=100, help_text='Enter your last name')
    email = forms.EmailField(max_length=150, help_text='Enter your email address')
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control',}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',) 

class ItemDayForm(forms.ModelForm):
    class Meta:
        model = ItemDay
        fields = ["note"]
	
	
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
	

class ItemTrackerForm(forms.ModelForm):
    class Meta:
        model = ItemTracker
        fields = ["item", "price", "debt", "description"]
	
	
