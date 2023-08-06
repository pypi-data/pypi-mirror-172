# pkmodel-zxara

TODO:
 - Usage section
 - 
A Python package for pharmacokinetics modelling of drug delivery systems.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install pkmodel-zxara
```

## Usage 

```python
import foobar
```

## Theory

Pharmacokinetics (PK) provides a quantitative basis for describing the delivery of a drug to a patient, the diffusion of that drug through the plasma/body tissue, and the subsequent clearance of the drug from the patient’s system. PK is used to ensure that there is sufficient concentration of the drug to maintain the required efficacy of the drug, while ensuring that the concentration levels remain below the toxic threshold. For an introductory theory, we recommend "Principles of Pharmacokinetics", by Ratain et. al. Available from: https://www.ncbi.nlm.nih.gov/books/NBK12815/

The model presented discretises the body into several linked, homogeneous compartments through which the concentration of an administered drug is tracked. It allows the user to specify the drug administration protocol, as well as physiological parameters.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
