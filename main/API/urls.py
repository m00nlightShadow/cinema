from rest_framework import routers
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from main.API.resources import HallViewSet, CinemaUserViewSet, MovieSessionViewSet, PurchaseViewSet, LogoutApiView

router = routers.DefaultRouter()
router.register(r'hall', HallViewSet)
router.register(r'user', CinemaUserViewSet)
router.register(r'movie-session', MovieSessionViewSet)
router.register(r'purchase', PurchaseViewSet)

urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', LogoutApiView.as_view()),
    path('', include(router.urls)),
]
