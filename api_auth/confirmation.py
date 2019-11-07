from urllib.parse import urlsplit

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core import signing
from django.urls import reverse

from chohankyun import settings


class EmailConfirmationHMAC:
    def __init__(self, email):
        self.email = email

    @property
    def key(self):
        return signing.dumps(obj=self.email, salt=getattr(settings, 'SALT', 'api_auth'))

    @classmethod
    def from_key(cls, key):
        try:
            max_age = (60 * 60 * 24 * getattr(settings, "EMAIL_CONFIRMATION_DAYS", 3))
            email = signing.loads(key, max_age=max_age, salt=getattr(settings, 'SALT', 'api_auth'))
            ret = cls(email)
        except (signing.SignatureExpired, signing.BadSignature, get_user_model().DoesNotExist):
            ret = None
        return ret

    def confirm(self):
        user = get_user_model().objects.filter(email=self.email).first()
        if not user.is_email_verified:
            user.is_email_verified = True
            user.save()
            return user

    def get_email_confirmation_url(self, request, confirmation):
        url = reverse("email_confirm", args=[confirmation.key])
        ret = self.build_absolute_uri(request, url)
        return ret

    @staticmethod
    def build_absolute_uri(request, location, protocol=None):
        default_protocol = getattr(settings, 'DEFAULT_HTTP_PROTOCOL', 'http').lower()

        if request is None:
            site = Site.objects.get_current()
            bits = urlsplit(location)
            if not (bits.scheme and bits.netloc):
                uri = '{proto}://{domain}{url}'.format(
                    proto=default_protocol,
                    domain=site.domain,
                    url=location)
            else:
                uri = location
        else:
            uri = request.build_absolute_uri(location)

        if not protocol and default_protocol == 'https':
            protocol = default_protocol

        if protocol:
            uri = protocol + ':' + uri.partition(':')[2]
        return uri
