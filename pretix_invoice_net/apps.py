from django.apps import AppConfig
from django.utils.translation import gettext_lazy
from . import __version__


class PluginApp(AppConfig):
    name = 'pretix_invoice_net'
    verbose_name = 'Pretix invoice renderer plugin for NETWAYS'

    class PretixPluginMeta:
        name = gettext_lazy('Pretix invoice renderer plugin for NETWAYS')
        author = 'NETWAYS GmbH'
        description = gettext_lazy('Pretix invoice renderer plugin for NETWAYS')
        visible = True
        version = __version__

    def ready(self):
        from . import signals  # NOQA
