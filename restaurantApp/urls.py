from django.urls import path
from .views import *

app_name = 'restaurantApp'

urlpatterns = [
    path('home/', index_view, name='home'),
    path('add-restaurant/', add_restaurant_view, name='add_restaurant'),
    path('edit-restaurant/<int:restaurant_id>/', edit_restaurant_view, name='edit_restaurant'),
    path('add-menu/<int:restaurant_id>/', add_menu_view, name='add_menu'),
    path('edit-menu/<int:menu_id>/', edit_menu_view, name='edit_menu'),
    path('add-menu-items/<int:menu_id>/', add_menu_item_view, name='add_menu_item'),
    path('edit-menu-items/<int:menu_item_id>/', edit_menu_item_view, name='edit_menu_item'),
    path('menu-items/<int:menu_id>/', menu_view, name='menu_view'),
    path('checkout/', checkout_view, name='checkout'),
    path('success/', payment_success, name='payment_success'),
    path('order/<str:item_id>/', order_view, name='order'),
    path('payment-process/<str:order_id>/', process_payment, name='process_payment'),

]
