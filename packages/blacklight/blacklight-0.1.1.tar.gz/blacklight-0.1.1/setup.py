# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['__init__', 'GDNN', 'GeneticTopologyFinder']
install_requires = \
['keras>=2.10.0,<3.0.0',
 'numpy>=1.23.4,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'scikit-learn>=1.1.2,<2.0.0',
 'scipy>=1.9.3,<2.0.0']

setup_kwargs = {
    'name': 'blacklight',
    'version': '0.1.1',
    'description': 'Genetic Deep Neural Net Topology Optimization',
    'long_description': '# GeneticDNN\nAn attempt to generalize neural network topology searches using genetic algorithms. \n',
    'author': 'Cole Agard',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
