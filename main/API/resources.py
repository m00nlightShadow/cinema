from django.contrib.auth.hashers import make_password
from django.db import transaction

from rest_framework import viewsets, permissions, serializers, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from main.API.serializers import HallSerializer, PurchaseSerializer, MovieSessionSerializer, \
    MovieSessionReadOnlySerializer, PurchaseReadOnlySerializer, UserRegisterSerializer, CinemaUserSerializer

from main.models import CinemaUser, Hall, Purchase, MovieSession


class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = [permissions.IsAdminUser]


class CinemaUserViewSet(viewsets.ModelViewSet):
    queryset = CinemaUser.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(id__in=[self.request.user.pk])
        return queryset

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = []
        elif self.action in ['list']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserRegisterSerializer
        return CinemaUserSerializer

    def perform_create(self, serializer):
        password = make_password(serializer.validated_data['password'])
        user = serializer.save(password=password)
        Token.objects.get_or_create(user=user)


class LogoutApiView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return PurchaseSerializer
        return PurchaseReadOnlySerializer

    def perform_create(self, serializer):
        movie_session = serializer.validated_data['movie_session']
        tickets_quantity = serializer.validated_data['tickets_quantity']
        user = self.request.user
        total_cost = movie_session.price * tickets_quantity

        if user.wallet < total_cost:
            raise serializers.ValidationError({'detail': 'You have not enough money'})

        user.wallet -= total_cost
        movie_session.tickets -= tickets_quantity

        with transaction.atomic():
            serializer.save(user=self.request.user, total_cost=total_cost)
            user.save()
            movie_session.save()


class MovieSessionViewSet(viewsets.ModelViewSet):
    queryset = MovieSession.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return MovieSessionSerializer
        return MovieSessionReadOnlySerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
