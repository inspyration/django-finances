"""# App configuration details"""


from importlib import import_module

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BankConfig(AppConfig):
    """Basic configuration class"""

    name = "bank"
    verbose_name = _("bank")

    def ready(self):
        import_module("{}.signals".format(self.name))
