from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from accounts.utils import token_generator
from django.contrib.auth import (
    authenticate,
    login,
    logout
)

# Create your views here.


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not token_generator(user, token):
                return redirect('frontend')

            user.is_active = True
            user.save()
        except Exception as ex:
            pass
        return redirect('frontend')
