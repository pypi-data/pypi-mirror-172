# Django Model Prefix
[![PyPI](https://badge.fury.io/py/django-model-prefix.svg)](https://pypi.org/project/django-model-prefix/)
[![Test Status](https://github.com/anexia/django-model-prefix/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/anexia/django-model-prefix/actions/workflows/tests.yml)
[![Codecov](https://codecov.io/gh/anexia/django-model-prefix/branch/main/graph/badge.svg)](https://codecov.io/gh/anexia/django-model-prefix)

A Django package that adds a global or model based database table prefix

# Installation

Install using pip:

```shell
pip install django-model-prefix
```

Add model_prefix to your INSTALLED_APPS list. Make sure it is the first app in the list

```python
INSTALLED_APPS = [
    'model_prefix',
    ...
]
```

# Usage

## Global table prefix

The global database table prefix can be configured using the `DB_PREFIX` setting

```python
DB_PREFIX = "foo_"
```

## Model table prefix

Optionally a model based prefix can also be defined by extending the models meta class

```python
class Meta:
    db_prefix = "bar_"
```

This can be also used in order to disable the global prefix for a specific model


```python
class Meta:
    db_prefix = None
```
