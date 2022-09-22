from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator


class UsernameValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+\- ]+$'
    message = _(
    'Enter a valid username. This value may contain only letters, '
    'numbers, whitespace, and @/./+/-/_ characters.'
    )


class User(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        help_text=_(
            'Required. 30 characters or fewer. Letters, digits, whitespace, and @/./+/-/_ only.'
        ),
        validators=[UsernameValidator()],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    email = models.EmailField('email address', unique=True, blank=False, null=False)
    is_online = models.BooleanField(default=False)
    last_online = models.DateTimeField(auto_now_add=True)
    disabled_until = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about_me = models.TextField(max_length=500, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='users/profile_pictures', null=True, blank=True)
    banner_image = models.ImageField(upload_to='users/banner_images', null=True, blank=True)
