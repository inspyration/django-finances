"""## App configuration details"""


from importlib import import_module

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TransactionConfig(AppConfig):
    """Basic configuration class"""

    name = "transaction"
    verbose_name = _("transaction")

    def ready(self):
        import_module("{}.signals".format(self.name))
