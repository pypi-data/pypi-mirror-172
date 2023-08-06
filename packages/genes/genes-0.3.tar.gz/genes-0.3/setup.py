# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genes',
 'genes.genalg',
 'genes.genalg.factoryd',
 'genes.genotype',
 'genes.genotype.genotyped',
 'genes.genotype.genotyped.error',
 'genes.genotype.operatord',
 'genes.genotype.populationd',
 'genes.stats']

package_data = \
{'': ['*']}

install_requires = \
['simple-value-object>=1.5,<2.0']

setup_kwargs = {
    'name': 'genes',
    'version': '0.3',
    'description': 'Simple library for playing with genetic algorithms',
    'long_description': 'None',
    'author': 'Łukasz Bacik',
    'author_email': 'mail@luka.sh',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
