# `measured`

`measured` is a library for measurements and quantities.

[![PyPi](https://img.shields.io/pypi/v/measured)](https://pypi.org/project/measured)
![Build and test](https://github.com/chrisguidry/measured/actions/workflows/build-and-test.yml/badge.svg?event=push)
[![Code Coverage](https://img.shields.io/codecov/c/github/chrisguidry/measured?flag=python-3.10)](https://app.codecov.io/gh/chrisguidry/measured/)
[![Documentation Status](https://readthedocs.org/projects/measured/badge/?version=latest)](https://measured.readthedocs.io/en/latest/?badge=latest)

```python
>>> from measured import Speed
>>> from measured.si import Meter, Second
>>> distance = 10 * Meter
>>> time = 2 * Second
>>> speed = distance / time
>>> assert speed == 5 * Meter / Second
>>> assert speed.unit == Meter / Second
>>> assert speed.unit.dimension == Speed
```

The goal of `measured` is to provide a sound foundation for recording and converting
physical quantities, while maintaining the integrity of their units and dimensions.

While it aims to be the fastest library of its kind, automatically tracking the units
and dimensions of quantities introduces significant overhead.  You can use `measured`
for applications where the accuracy of the units is more important than raw numerical
computing speed.

`measured` is licenced under the MIT Licence.

![MIT License](https://img.shields.io/github/license/chrisguidry/measured)

## Installing

`measured` is available on [PyPi](https://pypi.org/project/measured), and is tested with
with Python and PyPy 3.8+:

```bash
$ pip install measured
```
[![Python Versions](https://img.shields.io/pypi/pyversions/measured)](https://pypi.org/project/measured)

## Reference

The documentation for `measured` is on [Read the
Docs](https://measured.readthedocs.io/).

## Contributing

Contributions are welcome!  Please report bug and submit pull requests to
https://github.com/chrisguidry/measured.

[![Issues](https://img.shields.io/github/issues/chrisguidry/measured)](https://github.com/chrisguidry/measured/issues) [![Pull Requests](https://img.shields.io/github/issues-pr/chrisguidry/measured)](https://github.com/chrisguidry/measured/pulls)
