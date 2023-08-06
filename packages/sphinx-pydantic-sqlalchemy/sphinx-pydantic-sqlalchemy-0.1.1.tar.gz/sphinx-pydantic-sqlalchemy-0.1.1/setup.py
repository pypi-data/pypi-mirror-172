# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_pydantic_sqlalchemy']

package_data = \
{'': ['*']}

install_requires = \
['pydantic-sqlalchemy>=0.0.9,<0.0.10',
 'sphinx-jsonschema>=1.19.1,<2.0.0',
 'sphinx-pydantic>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'sphinx-pydantic-sqlalchemy',
    'version': '0.1.1',
    'description': 'Document SQLAlchemy models by leveraging to sphinx-pydantic and pydantic-sqlalchemy',
    'long_description': 'None',
    'author': 'David Francos',
    'author_email': 'davidfrancos@sipay.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
