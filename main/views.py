from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'main/home.html'


class UserLoginView(LoginView):
    template_name = 'main/login.html'

    def get_success_url(self):
        return reverse('home')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')
