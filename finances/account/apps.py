"""# App configuration details"""


from importlib import import_module

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AccountConfig(AppConfig):
    """Basic configuration class"""

    name = 'account'
    verbose_name = _("account")

    def ready(self):
        import_module("{}.signals".format(self.name))
