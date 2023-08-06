[![Test CI](https://github.com/mwhitemfldm/zxara_PK/actions/workflows/test-ci.yml/badge.svg)](https://github.com/mwhitemfldm/zxara_PK/actions/workflows/test-ci.yml)
[![OS Test](https://github.com/mwhitemfldm/zxara_PK/actions/workflows/test-os.yml/badge.svg)](https://github.com/mwhitemfldm/zxara_PK/actions/workflows/test-os.yml)
[![codecov](https://codecov.io/gh/mwhitemfldm/zxara_PK/branch/main/graph/badge.svg?token=QQLB4EFP0A)](https://codecov.io/gh/mwhitemfldm/zxara_PK)
[![Documentation Status](https://readthedocs.org/projects/zxara-pk/badge/?version=latest)](https://zxara-pk.readthedocs.io/en/latest/?badge=latest)


# pkmodel-zxara

A Python package for pharmacokinetics modelling of drug delivery systems.

Read the Docs [here](https://zxara-pk.readthedocs.io/en/latest/).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install pkmodel-zxara
```

## Usage 

Navigate to the model directory.

```
cd lib/python3.8/site-packages/pkmodel_zxara/
```

Run the __main__.py file.

```
python3 -m __main__.py
```

## Theory

Pharmacokinetics (PK) provides a quantitative basis for describing the delivery of a drug to a patient, the diffusion of that drug through the plasma/body tissue, and the subsequent clearance of the drug from the patient’s system. PK is used to ensure that there is sufficient concentration of the drug to maintain the required efficacy of the drug, while ensuring that the concentration levels remain below the toxic threshold. For an introductory theory, we recommend "Principles of Pharmacokinetics", by Ratain et. al. Available from: https://www.ncbi.nlm.nih.gov/books/NBK12815/

The model presented discretises the body into several linked, homogeneous compartments through which the concentration of an administered drug is tracked. It allows the user to specify the drug administration protocol, as well as physiological parameters.

## Demo

The program outputs a figure and the associated data. With these users may compare models with different protocols and physiological parameters. An example is provided in the results directory, as shown in the following figure.

<img src=results/Example_Figure.png width="700">

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
