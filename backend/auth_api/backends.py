from django.contrib.auth.backends import ModelBackend
from rest_framework.authtoken.models import Token

from users_api.models import User


class CustomModelBackend(ModelBackend):
    """ Custom authentication backend model that authenticates using
        email/password instead of username/password. """
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get(User.email)
        if email is None or password is None:
            return None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # run the hasher (see explanation in the parent model)
            User().set_password(password)
        else:
            if (user.check_password(password)
                    and self.user_can_authenticate(user)):
                return user
