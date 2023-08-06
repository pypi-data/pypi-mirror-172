[![License](https://img.shields.io/badge/license-Endeavour%20Mining-orange.svg)](https://github.com/endeavourmining/edv-dwh-connector/blob/master/LICENSE.txt)
[![codecov for extractors](https://codecov.io/gh/endeavourmining/edv-dwh-connector/branch/master/graph/badge.svg?token=c6I8wFFmZe)](https://codecov.io/gh/endeavourmining/edv-dwh-connector)

This project helps to connect to our data warehouse.

## Requirements

* Python `3.8.x` or later.


## Development environment

It is recommended to start by creating a virtual environment. You could do it by following commands:

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**N.B.** We activate an environment on Windows by executing:
```shell
.venv\Scripts\activate.bat
```

## How to contribute

Please read [contributing rules](https://github.com/endeavourmining/.github/blob/master/CONTRIBUTING.md).

Fork repository, make changes, send us a pull request. We will review
your changes and apply them to the `master` branch shortly, provided
they don't violate our quality standards. To avoid frustration, before
sending us your pull request please run these commands:

```shell
sh pyqulice.sh # Linux
pyqulice.bat # Windows
pytest tests/unit/
```
