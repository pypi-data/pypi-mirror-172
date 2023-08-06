# <img src='https://raw.githubusercontent.com/VicentePerezSoloviev/EDAspy/master/Logo%20EDAspy.png' align="right" height="150"/>

[![PyPI](https://img.shields.io/pypi/v/edaspy)](https://pypi.python.org/pypi/EDAspy/)
[![PyPI license](https://img.shields.io/pypi/l/EDAspy.svg)](https://pypi.python.org/pypi/EDAspy/)
[![Downloads](https://static.pepy.tech/personalized-badge/edaspy?period=total&units=none&left_color=grey&right_color=blue&left_text=downloads)](https://pepy.tech/project/edaspy)
[![Documentation Status](https://readthedocs.org/projects/edaspy/badge/?version=latest)](https://edaspy.readthedocs.io/en/latest/?badge=latest)

# EDAspy

## Introduction

EDAspy presents some implementations of the Estimation of Distribution Algorithms (EDAs). EDAs are a type of
evolutionary algorithms. Depending on the type of the probabilistic model embedded in the EDA, and the type of
variables considered, we will use a different EDA implementation.

The pseudocode of EDAs is the following:

1. Random initialization of the population.

2. Evaluate each individual of the population.

3. Select the top best individuals according to cost function evaluation.

4. Learn a probabilistic model from the best individuals selected.

5. Sampled another population.

6. If stopping criteria is met, finish; else, go to 2.

EDAspy allows to create a custom version of the EDA. Using the modular probabilistic models and the initializators, this can be embedded into the EDA baseline and used for different purposes. If this fits you, take a look on the examples section to the EDACustom example.

EDAspy also incorporates a set of benchmarks in order to compare the algorithms trying to minimize these cost functions.

The following implementations are available in EDAspy:

* UMDAd: Univariate Marginal Distribution Algorithm binary. It can be used as a simple example of EDA where the variables are binary and there are not dependencies between variables. Some usages include feature selection, for example.


* UMDAc: Univariate Marginal Distribution Algorithm continuous. In this EDA all the variables assume a Gaussian distribution and there are not dependencies considered between the variables. Some usages include hyperparameter optimization, for example.


* EGNA: Estimation of Gaussian Distribution Algorithm. This is a complex implementation in which dependencies between the variables are considered during the optimization. In each iteration, a Gaussian Bayesian network is learned and sampled. The variables in the model are assumed to be Gaussian and also de dependencies between them. This implementation is focused in continuous optimization.


* EMNA: Estimation of Multivariate Normal Algorithm. This is a similar implementation to EGNA, in which instead of using a Gaussian Bayesian network, a multivariate Gaussian distribution is iteratively learned and sampled. As in EGNA, the dependencies between variables are considered and assumed to be linear Gaussian. This implementation is focused in continuous optimization.


* Categorical EDA. In this implementation we consider some independent categorical variables. Some usages include portfolio optimization, for exampled.

## Examples

Some examples are available in https://github.com/VicentePerezSoloviev/EDAspy/tree/master/notebooks

## Getting started

For installing EDAspy from Pypi execute the following command using pip:

```bash
    pip install EDAspy
```

## Build from Source

### Prerequisites

- Python 3.6, 3.7, 3.8 or 3.9.
- Pybnesian, numpy, pandas.

### Building

Clone the repository:

```bash
    git clone https://github.com/VicentePerezSoloviev/EDAspy.git
    cd EDAspy
    git checkout v1.0.0 # You can checkout a specific version if you want
    python setup.py install
```
## Testing 

The library contains tests that can be executed using `pytest <https://docs.pytest.org/>`_. Install it using 
pip:

```bash
  pip install pytest
```

Run the tests with:

```bash
  pytest
```
