# from django.conf import settings
# from django.db import models
# from django.utils import timezone
# from django.utils.translation import gettext_lazy as _
# from .models import CustomUser
# from rest_framework.authtoken.models import Token

# class CustomTokenAuthentication(Token):
#     custom_created = models.DateTimeField(_('created'), default=timezone.now)
#     custom_user = models.ForeignKey(CustomUser, related_name='custom_tokens', on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = _('token')
#         verbose_name_plural = _('tokens')







# from .models import CustomUser
# from rest_framework import authentication
# from rest_framework import exceptions

# class ExampleAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         username = request.META.get('HTTP_X_USERNAME')
#         if not username:
#             return None

#         try:
#             user = CustomUser.objects.get(username=username)
#         except CustomUser.DoesNotExist:
#             raise exceptions.AuthenticationFailed('No such user')

#         return (user, None)






# users/token.py

from rest_framework.authentication import TokenAuthentication
from .models import CustomToken

class CustomTokenAuthentication(TokenAuthentication):
    model = CustomToken
