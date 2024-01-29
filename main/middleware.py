from datetime import timedelta, datetime

from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.conf import settings


class AutoLogoutMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated and not request.user.is_staff:
            last_action = request.session.get('last_action')
            if last_action:
                last_action = datetime.strptime(last_action, settings.DATETIME_LOGOUT_FORMAT)
            request.session['last_action'] = timezone.now().strftime(settings.DATETIME_LOGOUT_FORMAT)
            if last_action and timezone.now() - last_action > timedelta(seconds=settings.TIME_TO_LOGOUT):
                logout(request)
                return
