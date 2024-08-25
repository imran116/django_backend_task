from django import forms
from .models import Restaurant,Menu


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['restaurant_name', ]


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['menu_name','menu_desc']
