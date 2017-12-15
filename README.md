# Pretix Invoice Renderer Plugin for NETWAYS

This plugin adds a custom invoice renderer for NETWAYS hosted events and conferences
using <a href="https://pretix.eu/about/en/"><img src="https://github.com/NETWAYS/pretix-invoice-net/blob/master/res/logo.png" height="25"></a>.

Example order:

<img src="https://github.com/NETWAYS/pretix-invoice-net/blob/master/res/screenshot/pretix_invoice_net_event_order_pdf_table.png" alt="order table">


## Installation

https://pypi.python.org/pypi/pretix-invoice-net

### pip

```
pip install pretix-invoice-net
```

### Manual installation

```
cp -rv pretix-invoice-net/* /usr/src/pretix-invoice-net/
pip3 install /usr/src/pretix-invoice-net/
```

## Configuration

Navigate into the admin control panel and choose your event.

`Settings > Plugins` and enable the plugin.

<img src="https://github.com/NETWAYS/pretix-invoice-net/blob/master/res/screenshot/pretix_invoice_net_event_enable_plugin.png" alt="enable plugin" height="300">

`Settings > Invoicing` and choose the NETWAYS invoice renderer.

<img src="https://github.com/NETWAYS/pretix-invoice-net/blob/master/res/screenshot/pretix_invoice_net_event_select_renderer.png" alt="select renderer" height="300">

## Documentation

https://docs.pretix.eu/en/latest/development/api/plugins.html

Invoice renderer is inspired by [upstream](https://github.com/pretix/pretix/blob/master/src/pretix/base/invoice.py).

## Development setup

1. Make sure that you have a working [pretix development setup](https://docs.pretix.eu/en/latest/development/setup.html).
2. Clone this repository, eg to ``local/pretix-invoice-net``.
3. Activate the virtual environment you use for pretix development.
4. Execute ``python setup.py develop`` within this directory to register this application with pretix's plugin registry.
5. Execute ``make`` within this directory to compile translations.
6. Restart your local pretix server. You can now use the plugin from this repository for your events by enabling it in
   the 'plugins' tab in the settings.


# Thanks

Raphael Michel for Pretix and the initial invoice renderer code, which is adopted in this custom renderer plugin.

# License

Copyright 2017 NETWAYS GmbH <support@netways.de>
Copyright 2017 Raphael Michel <mail@raphaelmichel.de>

The code in this repository is published under the terms of the Apache License.
See the LICENSE file for the complete license text.
