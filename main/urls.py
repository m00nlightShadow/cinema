from django.contrib.auth.views import LogoutView
from django.urls import path

from main.views import (HomeView, UserLoginView,
                        UserLogoutView
                        )

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(next_page='/'), name='logout'),
]