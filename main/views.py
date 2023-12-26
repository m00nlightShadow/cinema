from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, FormView, UpdateView, DeleteView, DetailView
from main.forms import RegistrationForm, HallForm, MovieSessionForm, PurchaseForm
from main.mixins import StaffRequiredMixin
from main.models import MovieSession, Hall, Purchase, CinemaUser


class HomeView(ListView):
    template_name = 'main/home.html'
    model = MovieSession
    context_object_name = 'movie_sessions'
    extra_context = {'purchase_form': PurchaseForm}


class UserLoginView(LoginView):
    template_name = 'main/login.html'

    def get_success_url(self):
        return reverse('home')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'main/registration.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class CreateHallView(CreateView, StaffRequiredMixin):
    model = Hall
    form_class = HallForm
    template_name = 'main/create_hall.html'
    success_url = reverse_lazy('create_hall')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['halls'] = Hall.objects.filter(movie_session__isnull=True)
        return context


class UpdateHallView(UpdateView, StaffRequiredMixin):
    form_class = HallForm
    template_name = 'main/update_hall.html'
    success_url = reverse_lazy('create_hall')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_sessions'] = Hall.objects.filter(movie_session__isnull=True)
        return context


class CreateMovieSessionView(CreateView, StaffRequiredMixin):
    model = MovieSession
    form_class = MovieSessionForm
    template_name = 'main/create_movie_session.html'
    success_url = reverse_lazy('create_movie_session')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_sessions'] = MovieSession.objects.filter(purchase__isnull=True)
        return context


class UpdateMovieSessionView(UpdateView, StaffRequiredMixin):
    form_class = MovieSessionForm
    template_name = 'main/update_movie_session.html'
    success_url = reverse_lazy('create_movie_session')

    def get_queryset(self):
        return MovieSession.objects.filter(purchase__isnull=True)


class PurchaseView(LoginRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request, 'movie_session_pk': self.kwargs.get('pk')})
        return kwargs

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse('home'))

    def form_valid(self, form):
        movie_session = form.movie_session
        tickets_quantity = form.cleaned_data.get('tickets_quantity')
        total_price = movie_session.price * tickets_quantity
        purchase = form.save(commit=False)
        purchase.movie_session = movie_session
        purchase.user = self.request.user
        purchase.total_cost = total_price
        movie_session.tickets -= tickets_quantity
        self.request.user.wallet -= total_price
        with transaction.atomic():
            purchase.save()
            movie_session.save()
            self.request.user.save()
        messages.success(self.request, 'Successful!')
        return super().form_valid(form)


class MyPurchasesView(ListView, LoginRequiredMixin):
    template_name = 'main/my_tickets.html'
    model = Purchase
    context_object_name = 'purchases'

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_cost = sum(purchase.total_cost for purchase in context['purchases'])
        context['total_cost'] = total_cost
        return context
