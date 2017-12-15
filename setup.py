import os

from setuptools import setup, find_packages

try:
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except:
    long_description = ''

setup(
    name='pretix-invoice-net',
    version='0.0.1',
    description='Pretix invoice renderer plugin for NETWAYS',
    long_description=long_description,
    url='https://github.com/NETWAYS/pretix-invoice-net',
    author='NETWAYS GmbH',
    author_email='support@netways.de',
    license='Apache Software License',

    # pretix already depends on invoice related packages (reportlab, etc.)
    install_requires=[],
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    entry_points="""
[pretix.plugin]
pretix_invoice_net=pretix_invoice_net:PretixPluginMeta
""",
)
