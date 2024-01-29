from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils import timezone

from main.models import CinemaUser, Hall, Purchase, MovieSession


class CinemaUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = CinemaUser
        fields = ['id', 'username', 'email', ]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(read_only=True, source='auth_token.key')

    class Meta:
        model = CinemaUser
        fields = ['id', 'username', 'password', 'password2', 'token']

    def validate(self, attrs):
        if CinemaUser.objects.filter(username=attrs['username']).count():
            raise serializers.ValidationError("User with this username already exists")

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords are different")
        attrs.pop('password2')
        return attrs


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ['id', 'name', 'seats']


class MovieSessionReadOnlySerializer(serializers.ModelSerializer):
    hall = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MovieSession
        fields = ['id', 'start', 'end', 'hall', 'title', 'tickets', 'description', 'price']


class MovieSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSession
        fields = ['id', 'start', 'end', 'hall', 'title', 'tickets', 'description', 'price']

    def validate(self, data):
        start = data.get('start')
        end = data.get('end')
        hall = data.get('hall')
        tickets = data.get('tickets')

        if tickets is not None and (tickets > hall.seats or tickets == 0):
            raise serializers.ValidationError('The number of tickets must not exceed the number of seats in the hall')

        if MovieSession.objects.filter(hall=hall, start__lte=end, end__gte=start).exists():
            raise serializers.ValidationError("The session overlaps with another session. Please choose another time")

        if start >= end:
            raise serializers.ValidationError('Movie session can not starts before ends')

        if start < timezone.now():
            raise serializers.ValidationError('You cannot start movie session in the past.')

        return data


class PurchaseReadOnlySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    movie_session = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Purchase
        fields = ['id', 'user', 'movie_session', 'tickets_quantity', 'total_cost']


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'user', 'movie_session', 'tickets_quantity', 'total_cost']
        read_only_fields = ['user']

    def validate(self, data):
        movie_session = data.get('movie_session')
        tickets_quantity = data.get('tickets_quantity')
        available_tickets = movie_session.tickets

        if tickets_quantity < 1:
            raise serializers.ValidationError('Please choose at least one ticket')

        if tickets_quantity > available_tickets:
            raise serializers.ValidationError('Not enough tickets for purchase')

        return data
