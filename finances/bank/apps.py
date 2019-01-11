"""# App configuration details"""


from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BankConfig(AppConfig):
    """Basic configuration class"""

    name = "bank"
    verbose_name = _("bank")
