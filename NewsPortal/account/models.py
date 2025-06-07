from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import User

class Users(User):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=20,
        unique=True,
        help_text=_('Required. 20 characters or fewer. '
                    'Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    password = models.CharField(_('password'), max_length=128)
    nick_name = models.CharField(_('nick name'), max_length=16,)
    email = models.EmailField(_('email adress'), blank=True)
