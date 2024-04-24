from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from accounts.managers import UserManager


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=11, unique=True, verbose_name=_('Phone Number'))
    address = models.TextField(verbose_name=_('Address'))
    username = models.CharField(
        _("username"),
        max_length=150,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        null=True,
        blank=True,
    )
    USERNAME_FIELD = 'email'
    objects = UserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class VerifictionOtp(models.Model):
    class VerificationType(models.TextChoices):
        REGISTER = 'register', _('Register')
        RESET_PASSWORD = 'reset_password', _('Reset password')

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='verification_otp')
    code = models.IntegerField(_('Otp code'))
    type = models.CharField(_('Verification type'), choices=VerificationType.choices, max_length=60)
    expires_in = models.DateTimeField(_('Expiration time'))

    def __str__(self):
        return f"{self.user.email} | code: {self.code}"

    class Meta:
        verbose_name = _('Verification Otp')
        verbose_name_plural = _('Verification Otps')


class UserAddress(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user_address')
    name = models.CharField(_('Name'), max_length=150)
    phone_number = models.CharField(_('Phone Number'), max_length=20)
    apartment = models.CharField(_('Apartment'), max_length=150)
    street = models.TextField(_('Street'), max_length=150)
    pin_code = models.CharField(_('Pin Code'), max_length=120)
    # city = models.ForeignKey()

    def __str__(self):
        return f'{self.user.id} {self.name}'

    class Meta:
        verbose_name = _('User Address')
        verbose_name_plural = _('User Addresses')
