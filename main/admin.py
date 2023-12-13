from django.contrib import admin
from .models import CinemaUser, Hall, Purchase, Session, Movie

admin.site.register(CinemaUser)
admin.site.register(Hall)
admin.site.register(Purchase)
admin.site.register(Session)
admin.site.register(Movie)
