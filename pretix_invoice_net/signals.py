# Pretix Invoice Renderer for NETWAYS
#
# Copyright 2017 NETWAYS GmbH <support@netways.de>
# Copyright 2017 Raphael Michel <mail@raphaelmichel.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.dispatch import receiver

from pretix.base.signals import register_invoice_renderers

@receiver(register_invoice_renderers, dispatch_uid="output_netways")
def recv_net(sender, **kwargs):
    from .invoice import NetInvoiceRenderer
    return NetInvoiceRenderer
