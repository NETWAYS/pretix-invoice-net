# Pretix Invoice Renderer Plugin for NETWAYS

This is a plugin for [pretix](https://github.com/pretix/pretix) made for the NETWAYS environment.

It adds a custom invoice renderer for NETWAYS hosted events.


## Installation

```
cp -rv pretix-invoice-net/* /usr/src/pretix-invoice-net/
pip3 install /usr/src/pretix-invoice-net/
```

Future plans involve publishing on pypi.python.org

## Documentation

https://docs.pretix.eu/en/latest/development/api/plugins.html

Invoice renderer is inspired by [upstream](https://github.com/pretix/pretix/blob/master/src/pretix/base/invoice.py).

## Development setup

1. Make sure that you have a working [pretix development setup](https://docs.pretix.eu/en/latest/development/setup.html).
2. Clone this repository, eg to ``local/pretix-net``.
3. Activate the virtual environment you use for pretix development.
4. Execute ``python setup.py develop`` within this directory to register this application with pretix's plugin registry.
5. Execute ``make`` within this directory to compile translations.
6. Restart your local pretix server. You can now use the plugin from this repository for your events by enabling it in
   the 'plugins' tab in the settings.

### Create release tarball

```
python setup.py sdist
```

# Thanks

Raphael Michel for Pretix and the initial invoice renderer code, which is adopted in this custom renderer plugin.

# License


Copyright 2017 Raphael Michel <mail@raphaelmichel.de>
Copyright 2017 NETWAYS GmbH <support@netways.de>

The code in this repository is published under the terms of the Apache License.
See the LICENSE file for the complete license text.
