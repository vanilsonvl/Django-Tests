import base64
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from tastypie.http import HttpUnauthorized

__author__ = 'Matheus'


from tastypie.authentication import Authentication


class EmailAuthentication(Authentication):
    def __init__(self, backend=None, realm='django-tastypie', **kwargs):
        super(EmailAuthentication, self).__init__(**kwargs)
        self.backend = backend
        self.realm = realm

    def _unauthorized(self):
        response = HttpUnauthorized()
        # FIXME: Sanitize realm.
        response['WWW-Authenticate'] = 'Basic Realm="%s"' % self.realm
        return response

    def is_authenticated(self, request, **kwargs):
        if not request.META.get('HTTP_AUTHORIZATION'):
            return self._unauthorized()

        try:
            (auth_type, data) = request.META['HTTP_AUTHORIZATION'].split()
            if auth_type.lower() != 'basic':
                return self._unauthorized()
            user_pass = base64.b64decode(data).decode('utf-8')
        except:
            return self._unauthorized()

        bits = user_pass.split(':', 1)

        if len(bits) != 2:
            return self._unauthorized()

        username = User.objects.get(email=bits[0]).username

        if self.backend:
            user = self.backend.authenticate(username=username, password=bits[1])
        else:
            user = authenticate(username=username, password=bits[1])

        if user is None:
            return self._unauthorized()

        if not self.check_active(user):
            return False

        request.user = user
        return True

    def get_identifier(self, request):
        return request.user.username