from django.contrib.auth.models import AbstractUser
from django.db import models


class CinemaUser(AbstractUser):
    pass


class Hall(models.Model):
    name = models.CharField(max_length=100)
    seats = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.name} - {self.size} seats'


class Movie(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return {self.title}


class Session(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='session_hall')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='session_movie')
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.movie} starts at {self.start}, ends at {self.end}'


class Purchase(models.Model):
    user = models.ForeignKey(CinemaUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
