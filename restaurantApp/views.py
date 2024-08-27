from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import RestaurantForm, MenuForm, MenuItemForm
from .models import Restaurant, Menu, MenuItem, Order
import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


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
        'restaurant_obj': restaurant_obj,
    })


def edit_menu_view(request, menu_id):
    menu_obj = Menu.objects.get(pk=menu_id)
    if request.method == "POST":
        form = MenuForm(request.POST, instance=menu_obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('restaurantApp:add_menu', args=[menu_obj.restaurant.id]))
    else:
        form = MenuForm(instance=menu_obj)
    return render(request, 'restaurant/edit-menu.html', {'form': form})


def add_menu_item_view(request, menu_id):
    menu_obj = Menu.objects.get(pk=menu_id)
    all_menu_items = MenuItem.objects.filter(menu=menu_obj)
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        menuItems = form.save(commit=False)
        menuItems.menu = menu_obj
        menuItems.save()
        return redirect(reverse('restaurantApp:add_menu_item', args=[menu_id]))
    else:
        form = MenuItemForm()
    return render(request, 'restaurant/add-menu-item.html',
                  {'form': form, 'all_menu_items': all_menu_items, 'menu_obj': menu_obj})


def edit_menu_item_view(request, menu_item_id):
    menu_item_obj = MenuItem.objects.get(pk=menu_item_id)
    if request.method == "POST":
        form = MenuItemForm(request.POST, instance=menu_item_obj)
        form.save()
        return redirect(reverse('restaurantApp:add_menu_item', args=[menu_item_obj.menu.id]))
    else:
        form = MenuItemForm(instance=menu_item_obj)
    return render(request, 'restaurant/edit-menu-item.html', {'form': form, })


def menu_view(request, menu_id):
    menu_obj = Menu.objects.get(pk=menu_id)
    menu_list = MenuItem.objects.filter(menu=menu_obj)

    return render(request, 'restaurant/view-menu.html', {'menu_lists': menu_list, 'menu_obj': menu_obj})


def checkout_view(request):
    return render(request, 'checkout/checkout.html')


def payment_success(request):
    return render(request, 'checkout/payment_success.html')


def process_payment(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(MenuItem, id=order_id)
        token = request.POST.get('stripeToken')

        try:
            customer = stripe.Customer.create(
                email=request.user.email,
                source=token

            )

            charge = stripe.Charge.create(
                customer=customer.id,
                amount=int(order.menu_items_price * 100),
                currency='usd',
                description=f"Order #{order.id} Payment success",

            )

            order.stripe_customer_id = customer.id
            order.paid = True
            order.save()

            return redirect('restaurantApp:payment_success')
        except stripe.error.CardError as e:

            return JsonResponse({'status': 'failed', 'message': str(e)}, status=400)

    return render(request, 'checkout/checkout.html')


def order_view(request, item_id):
    get_menu_list = MenuItem.objects.get(id=item_id)

    order = Order.objects.create(
        user=request.user,
        restaurant_name=get_menu_list.menu.restaurant.restaurant_name,
        menu_name=get_menu_list.menu.menu_name,
        menu_item_name=get_menu_list.menu_items_name,
        menu_item_desc=get_menu_list.menu_items_desc,
        menu_item_price=get_menu_list.menu_items_price,
    )
    order.save()
    return render(request, 'checkout/checkout.html', {'order': order})
