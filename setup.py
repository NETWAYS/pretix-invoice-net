import os

from setuptools import setup, find_packages

# pypi doesn't like markdown, it needs RST.
# https://stackoverflow.com/questions/26737222/pypi-description-markdown-doesnt-work
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except:
    long_description = open('README.md').read()

setup(
    name = 'pretix-invoice-net',
    version = '0.0.3',
    description = 'Pretix invoice renderer plugin for NETWAYS',
    long_description = long_description,
    url = 'https://github.com/NETWAYS/pretix-invoice-net',
    download_url = 'https://github.com/NETWAYS/pretix-invoice-net/archive/v0.0.3.tar.gz',
    keywords = [ 'pretix', 'tickets', 'events', 'invoice', 'pdf' ],
    author = 'NETWAYS GmbH',
    author_email = 'support@netways.de',
    license = 'Apache Software License',

    # pretix already depends on invoice related packages (reportlab, etc.)
    install_requires=[],
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    entry_points="""
[pretix.plugin]
pretix_invoice_net=pretix_invoice_net:PretixPluginMeta
""",
)
