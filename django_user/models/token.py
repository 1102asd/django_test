import binascii
import os
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class ApiToken(models.Model):
    """
    The default authorization token model that supports expiration.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='api_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    expires = models.DateTimeField(_("Expires"), auto_now_add=True)

    class Meta:
        db_table = 'sso2_apitoken'
        verbose_name = _("APIToken")
        verbose_name_plural = _("APITokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ApiToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def is_expired(self):
        return timezone.now() > self.expires

    def set_max_age(self, days=1):
        new_expires = timezone.now() + timedelta(days=days)
        # We only extend the expires, not to shorten it
        if new_expires > self.expires:
            self.expires = new_expires

    def set_max_age_seconds(self, seconds=7200):
        new_expires = timezone.now() + timedelta(seconds=seconds)
        # We only extend the expires, not to shorten it
        if new_expires > self.expires:
            self.expires = new_expires

    def __str__(self):
        return self.key
