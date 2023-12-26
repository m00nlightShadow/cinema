from django.utils import timezone

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateTimeInput
from django.contrib import messages

from main.models import CinemaUser, Hall, MovieSession, Purchase


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = CinemaUser
        fields = ['username']
        widgets = {
            'email': forms.EmailInput(),
            'password': forms.PasswordInput(),
        }


class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = '__all__'


class MovieSessionForm(forms.ModelForm):
    class Meta:
        model = MovieSession
        fields = '__all__'

        widgets = {
            'start': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end': DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start')
        end_time = cleaned_data.get('end')
        tickets = cleaned_data.get('tickets')
        hall_seats = cleaned_data.get('hall').seats

        if tickets is not None and (tickets > hall_seats or tickets == 0):
            raise ValidationError('The number of tickets must not exceed the number of seats in the hall')

        if start_time and end_time:
            overlapping_sessions = MovieSession.objects.filter(
                hall=cleaned_data.get('hall'),
                start__lt=end_time,
                end__gt=start_time
            ).exclude(pk=self.instance.pk)

            if overlapping_sessions.exists():
                raise ValidationError('The session overlaps with another session. Please choose another time')

            if start_time >= end_time:
                raise ValidationError('Movie session can not starts before ends')

            if start_time < timezone.now():
                raise ValidationError('You cannot start movie session in the past.')
        return cleaned_data


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['tickets_quantity', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.movie_session_pk = kwargs.pop('movie_session_pk', None)
        super().__init__(*args, **kwargs)
        self.fields['tickets_quantity'].label = 'Buy tickets'

    def clean(self):
        cleaned_data = super().clean()
        try:
            movie_session = MovieSession.objects.get(pk=self.movie_session_pk)
            self.movie_session = movie_session
        except MovieSession.DoesNotExist:
            messages.error(self.request, 'Session does not exist')
            raise ValidationError('Incorrect session id')
        tickets_quantity = cleaned_data['tickets_quantity']
        if movie_session.tickets < tickets_quantity:
            messages.error(self.request, 'Not enough tickets')
            self.add_error('tickets_quantity', 'Not enough tickets')
        if not tickets_quantity:
            messages.error(self.request, "You can't buy 0 tickets")
            self.add_error('tickets_quantity', "You can't buy 0 tickets")
