from django.urls import path
from .views import *

urlpatterns = [
    path('sign-up/', sign_up_view, name='sign_up'),
    path('login/', login_view.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
