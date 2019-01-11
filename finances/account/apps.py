"""# App configuration details"""


from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AccountConfig(AppConfig):
    """Basic configuration class"""

    name = 'account'
    verbose_name = _("account")
