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
    'version': '0.6.1',
    'description': 'Pharmacokinetic modelling of drug delivery',
    'long_description': '# pkmodel-zxara\n\nTODO:\n - Usage section\n \nA Python package for pharmacokinetics modelling of drug delivery systems.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install.\n\n```bash\npip install pkmodel-zxara\n```\n\n## Usage \n\nIn a Python shell import the model library. *Emphasis on the underscore in the library name*.\n\n```python\nimport pkmodel_zxara\n```\n\n## Theory\n\nPharmacokinetics (PK) provides a quantitative basis for describing the delivery of a drug to a patient, the diffusion of that drug through the plasma/body tissue, and the subsequent clearance of the drug from the patient’s system. PK is used to ensure that there is sufficient concentration of the drug to maintain the required efficacy of the drug, while ensuring that the concentration levels remain below the toxic threshold. For an introductory theory, we recommend "Principles of Pharmacokinetics", by Ratain et. al. Available from: https://www.ncbi.nlm.nih.gov/books/NBK12815/\n\nThe model presented discretises the body into several linked, homogeneous compartments through which the concentration of an administered drug is tracked. It allows the user to specify the drug administration protocol, as well as physiological parameters.\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Anissa Alloula',
    'author_email': 'anissa.alloula@dtc.ox.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mwhitemfldm/zxara_PK',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
