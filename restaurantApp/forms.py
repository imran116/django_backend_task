from django import forms
from .models import Restaurant, Menu, MenuItem


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['restaurant_name', ]


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['menu_name', 'menu_desc']


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['menu_items_name', 'menu_items_desc', 'menu_items_price']
