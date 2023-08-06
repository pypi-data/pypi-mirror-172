# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pkmodel_zxara', 'pkmodel_zxara.tests']

package_data = \
{'': ['*']}

install_requires = \
['attrs==22.1.0',
 'contourpy==1.0.5',
 'cycler==0.11.0',
 'fonttools==4.37.4',
 'iniconfig==1.1.1',
 'kiwisolver==1.4.4',
 'matplotlib==3.6.1',
 'numpy==1.23.4',
 'packaging==21.3',
 'pillow==9.2.0',
 'pluggy==1.0.0',
 'py==1.11.0',
 'pyparsing==3.0.9',
 'python-dateutil==2.8.2',
 'scipy==1.9.2',
 'six==1.16.0',
 'tomli==2.0.1']

setup_kwargs = {
    'name': 'pkmodel-zxara',
    'version': '0.2.0',
    'description': 'A pharmacokinetic model',
    'long_description': '# 2020-software-engineering-projects-pk\nstarter pk modelling repository\n',
    'author': 'Jacob Wright',
    'author_email': 'jacob.wright@dtc.ox.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
