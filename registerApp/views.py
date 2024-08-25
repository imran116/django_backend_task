from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render,redirect
from .forms import UserRegistrationForm, UserLoginForm
from .models import Profile



# Create your views here.

def sign_up_view(request):
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            Profile.objects.create(
                user=user,
                phone=phone,
                address=address,
            )
            return render(request, 'restaurant/restaurant-list.html')

    return render(request, 'register/sign-up.html',{'form':form})

class login_view(LoginView):
    form_class = UserLoginForm
    template_name = 'register/login.html'

    def get_success_url(self):
        return redirect('restaurantApp:home').url

def logout_view(request):
    logout(request)
    return render(request, 'register/sign-up.html')
