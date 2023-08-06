# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['lospec2css']
setup_kwargs = {
    'name': 'lospec2css',
    'version': '0.1.0',
    'description': 'Convert lospec color palette files into CSS files.',
    'long_description': None,
    'author': 'Rob Wagner',
    'author_email': 'rob@sombia.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
