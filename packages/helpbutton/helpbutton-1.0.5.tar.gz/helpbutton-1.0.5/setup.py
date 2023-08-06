# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['helpbutton']
install_requires = \
['discord>=2.0.0,<3.0.0', 'typing>=3.7.4.3,<4.0.0.0']

setup_kwargs = {
    'name': 'helpbutton',
    'version': '1.0.5',
    'description': '',
    'long_description': 'My',
    'author': 'Sad_Cat0326',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
