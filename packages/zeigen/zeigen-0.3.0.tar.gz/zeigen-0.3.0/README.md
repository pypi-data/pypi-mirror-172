# Zeigen - Show Water Networks

[![PyPI](https://img.shields.io/pypi/v/zeigen.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/zeigen)][pypi status]
[![Docs](https://img.shields.io/readthedocs/zeigen/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/hydrationdynamics/zeigen/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/hydrationdynamics/zeigen/branch/main/graph/badge.svg)][codecov]
[![Repo](https://img.shields.io/github/last-commit/hydrationdynamics/zeigen)][repo]
[![Downloads](https://pepy.tech/badge/zeigen)][downloads]
[![Dlrate](https://img.shields.io/pypi/dm/zeigen)][dlrate]
[![Codacy](https://app.codacy.com/project/badge/Grade/3e29ba5ba23d48888372138790ab26f3)][codacy]
[![Snyk Health](https://snyk.io/advisor/python/zeigen/badge.svg)][snyk]

[pypi status]: https://pypi.org/project/zeigen/
[read the docs]: https://zeigen.readthedocs.io/
[tests]: https://github.com/hydrationdynamics/zeigen/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/hydrationdynamics/zeigen
[repo]: https://github.com/hydrationdynamics/zeigen
[downloads]: https://pepy.tech/project/zeigen
[dlrate]: https://github.com/hydrationdynamics/zeigen
[codacy]: https://www.codacy.com/gh/hydrationdynamics/zeigen?utm_source=github.com&utm_medium=referral&utm_content=hydrationdynamics/zeigen&utm_campaign=Badge_Grade
[snyk]: https://snyk.io/advisor/python/zeigen

[![logo](https://raw.githubusercontent.com/hydrationdynamics/zeigen/main/docs/_static/logo.png)][logo license]

[logo license]: https://raw.githubusercontent.com/hydrationdynamics/zeigen/main/LICENSE.logo.txt

## Features

_Zeigen_ finds networks of water in PDB structures.
The PDB query is highly configurable through the `zeigen.conf`
configuration file that is placed in the config
directory upon first program run. The query results are
placed in a TSV file, with global stats to a JSON file.

_Zeigen_ uses _rcsbsearch_ to query the PDB. Currently the
_rcsbsearch_ package is broken, as it uses the obsolete v1
query. _Zeigen_ includes a copy of _rcsbsearch_ which has
been patched for v2 queries.

## Requirements

_Zeigen_ has been developed under Python 3.10 and
tested on Python 3.9 and 3.10 on Linux. Works on MacOS, but
not tested due to energy costs.

## Installation

You can install _Zeigen_ via [pip] from [PyPI]:

```console
$ pip install zeigen
```

## Usage

Please see the [Command-line Reference] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [BSD 3-Clause license][license],
_Zeigen_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

_Zeigen_ was written by Joel Berendzen.

_rcsbsearch_ was written by Spencer Bliven.

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/hydrationdynamics/zeigen/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/hydrationdynamics/zeigen/blob/main/LICENSE
[contributor guide]: https://github.com/hydrationdynamics/zeigen/blob/main/CONTRIBUTING.md
[command-line reference]: https://zeigen.readthedocs.io/en/latest/usage.html
