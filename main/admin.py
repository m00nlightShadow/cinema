from django.contrib import admin
from .models import CinemaUser, Hall, Purchase, MovieSession

admin.site.register(CinemaUser)
admin.site.register(Hall)
admin.site.register(Purchase)
admin.site.register(MovieSession)
