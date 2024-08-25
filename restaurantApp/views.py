from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import RestaurantForm, MenuForm
from .models import Restaurant, Menu


# Create your views here.

def index_view(request):
    all_restaurant_lists = Restaurant.objects.all()

    return render(request, 'index/index.html', {'all_restaurant_lists': all_restaurant_lists})


def add_restaurant_view(request):
    restaurant_lists = Restaurant.objects.filter(owner=request.user.profile)
    all_restaurant_lists = Restaurant.objects.all()
    form = RestaurantForm()
    if request.method == 'POST':

        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurants = form.save(commit=False)
            restaurants.owner = request.user.profile
            restaurants.save()
            return render(request, "restaurant/restaurant-list.html", {
                'restaurant_lists': restaurant_lists,
                'all_restaurant_lists': all_restaurant_lists,
                'form': form
            })

    return render(request, 'restaurant/restaurant-list.html', {
        'form': form,
        'all_restaurant_lists': all_restaurant_lists,
        'restaurant_lists': restaurant_lists,
    })


def edit_restaurant_view(request, restaurant_id):
    restaurant_obj = Restaurant.objects.get(id=restaurant_id)
    if request.method == "POST":
        form = RestaurantForm(request.POST, instance=restaurant_obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('restaurantApp:add_restaurant'))
    else:
        form = RestaurantForm(instance=restaurant_obj)
    return render(request, 'restaurant/edit-restaurant-list.html', {'form': form})


def add_menu_view(request, restaurant_id):
    restaurant_obj = Restaurant.objects.get(id=restaurant_id)
    all_menu_list = Menu.objects.filter(restaurant=restaurant_obj)
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.restaurant = restaurant_obj
            menu.save()
            return redirect(reverse('restaurantApp:add_menu', args=[restaurant_id]))
    else:
        form = MenuForm()

    return render(request, 'restaurant/add-menu.html', {
        'form': form,
        'all_menu_lists': all_menu_list,
        'restaurant_obj':restaurant_obj,
    })

def edit_menu_view(request, menu_id):
    menu_obj = Menu.objects.get(pk=menu_id)
    if request.method == "POST":
        form = MenuForm(request.POST, instance=menu_obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('restaurantApp:add_menu',args=[menu_obj.restaurant.id]))
    else:
        form = MenuForm(instance=menu_obj)
    return render(request, 'restaurant/edit-menu.html',{'form':form})

