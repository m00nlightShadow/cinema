from django.contrib.auth.models import AbstractUser
from django.db import models


class CinemaUser(AbstractUser):
    pass


class Hall(models.Model):
    name = models.CharField(max_length=100)
    seats = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name} - {self.seats} seats'


class MovieSession(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='movie_session')
    title = models.CharField(max_length=100)
    tickets = models.PositiveIntegerField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.title} starts at {self.start}, ends at {self.end}'


class Purchase(models.Model):
    user = models.ForeignKey(CinemaUser, on_delete=models.CASCADE)
    movie_session = models.ForeignKey(MovieSession, on_delete=models.CASCADE)
    tickets_quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.tickets_quantity} tickets for {self.user} to {self.movie_session}'
