import datetime
from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils.deprecation import MiddlewareMixin

class UpdateLastActivityMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            now = datetime.datetime.now()
            request.session['last_activity'] = now.timestamp()

class CheckLastActivityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            now = datetime.datetime.now().timestamp()
            if last_activity and (now - last_activity) > settings.SESSION_COOKIE_AGE:
                Session.objects.filter(pk=request.session.session_key).delete()
