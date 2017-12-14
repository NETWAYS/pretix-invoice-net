from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class PluginApp(AppConfig):
    name = 'pretix_invoice_net'
    verbose_name = 'Pretix invoice renderer plugin for NETWAYS'

    class PretixPluginMeta:
        name = ugettext_lazy('Pretix invoice renderer plugin for NETWAYS')
        author = 'NETWAYS GmbH'
        description = ugettext_lazy('Pretix invoice renderer plugin for NETWAYS')
        visible = True
        version = '1.0.0'

    def ready(self):
        from . import signals  # NOQA


default_app_config = 'pretix_invoice_net.PluginApp'
