from django.contrib.auth.views import LogoutView
from django.urls import path

from main.views import (HomeView, UserLoginView,
                        UserLogoutView, RegistrationView, CreateHallView, CreateMovieSessionView, PurchaseView,
                        MyPurchasesView, UpdateHallView, UpdateMovieSessionView,
                        )

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('create-hall', CreateHallView.as_view(), name='create_hall'),
    path('create-movie-session', CreateMovieSessionView.as_view(), name='create_movie_session'),
    path('buy-tickets/<int:pk>/', PurchaseView.as_view(), name='buy_tickets'),
    path('my-tickets/', MyPurchasesView.as_view(), name='my_tickets'),
    path('update-hall/<int:pk>/', UpdateHallView.as_view(), name='update_hall'),
    path('update-movie-session/<int:pk>/', UpdateMovieSessionView.as_view(), name='update_movie_session'),

]
