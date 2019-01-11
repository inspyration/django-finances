"""# App configuration details"""


from importlib import import_module

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SourceConfig(AppConfig):
    """Basic configuration class"""

    name = 'source'
    verbose_name = _("source")

    def ready(self):
        import_module("{}.signals".format(self.name))
