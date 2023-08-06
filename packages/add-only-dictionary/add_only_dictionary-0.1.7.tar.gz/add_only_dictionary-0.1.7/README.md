# Add Only Dictionary

[![PyPI](https://img.shields.io/pypi/v/add-only-dictionary.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/add-only-dictionary.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/add-only-dictionary)][python version]
[![License](https://img.shields.io/pypi/l/add-only-dictionary)][license]

[![Read the documentation at https://add-only-dictionary.readthedocs.io/](https://img.shields.io/readthedocs/add-only-dictionary/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/maccam912/add-only-dictionary/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/maccam912/add-only-dictionary/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/add-only-dictionary/
[status]: https://pypi.org/project/add-only-dictionary/
[python version]: https://pypi.org/project/add-only-dictionary
[read the docs]: https://add-only-dictionary.readthedocs.io/
[tests]: https://github.com/maccam912/add-only-dictionary/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/maccam912/add-only-dictionary
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Features

- Create dictionaries that let you continue adding key/value pairs, but never change existing values or remove existing keys. If a value is a dictionary, that will also be updated to have the same behavior. If the value is a list, items can only be added on to the list, but never removed from any position.

## Installation

You can install _Add Only Dictionary_ via [pip] from [PyPI]:

```console
$ pip install add-only-dictionary
```

## Usage

```python
from add_only_dictionary import AODict

regular_dict: Dict = {"a": 1}
ao_dict: AODict = AODict(regular_dict)

ao_dict["b"] = 2 # works!
ao_dict["a"] = 3 # Nothing happens...
ao_dict["a"] == 1 # True, since the key already existed.
```

<!-- ## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Add Only Dictionary_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description. -->

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/maccam912/add-only-dictionary/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/maccam912/add-only-dictionary/blob/main/LICENSE
[contributor guide]: https://github.com/maccam912/add-only-dictionary/blob/main/CONTRIBUTING.md
[command-line reference]: https://add-only-dictionary.readthedocs.io/en/latest/usage.html
