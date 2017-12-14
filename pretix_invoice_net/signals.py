# Register your receivers here

from django.dispatch import receiver

from pretix.base.signals import register_invoice_renderers

@receiver(register_invoice_renderers, dispatch_uid="output_netways")
def recv_net(sender, **kwargs):
    from .invoice import NetInvoiceRenderer
    return NetInvoiceRenderer
