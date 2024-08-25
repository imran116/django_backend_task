from django.urls import path
from .views import *

app_name = 'restaurantApp'

urlpatterns = [
    path('home/', index_view, name='home'),
    path('add-restaurant/', add_restaurant_view, name='add_restaurant'),
    path('edit-restaurant/<int:restaurant_id>/', edit_restaurant_view, name='edit_restaurant'),
    path('add-menu/<int:restaurant_id>/', add_menu_view, name='add_menu'),
    path('edit-menu/<int:menu_id>/', edit_menu_view, name='edit_menu'),

]
