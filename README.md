# Airborne CLI

> Note: This project is **still** under active development/testing.

[![Python Version](https://img.shields.io/badge/python-%3E=3.10-blue?style=for-the-badge&logo=python&logoColor=white)][python version]
[![License](https://img.shields.io/github/license/drearondov/airborne-cli?style=for-the-badge)][license]
[![Tests](https://github.com/drearondov/airborne-cli/workflows/Tests/badge.svg)][tests]
[![Codecov](https://img.shields.io/codecov/c/github/drearondov/airborne-cli?style=for-the-badge&logo=codecov&logoColor=white)][codecov]
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=for-the-badge)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)][black]

A CLI utility to use the [airborne.cam] app to process several rooms at once,
under multiple conditions from an input file size.

## Features

- Support to process data in a `.xlsx`, `.csv` or `.json` format
- Fully configurable default mode for fast running
- Exports graphics in `png` and `html`(coming soon) format for risk analysis.

## Requirements

To install and use the program `Python >= 3.10` is required.

## Install

> Note: This package is still under development, and as such it has not been
> published to [PyPI]. Also, because of the nature of the package I haven't
> decided if it'll ever be.

### Package instalation

If you still would like to use this tools, you can get the latest version of
_Airborne CLI_ following this steps.

```bash
repo='https://github.com/drearondov/airborne-cli'

# Find the latest release.
latest=$(git ls-remote --tags --refs $repo | # Fetch remote tags.
                 sort -t '/' -k 3 -V |       # Sort them by version.
                 tail -n 1 |                 # Take the latest one.
                 awk -F / '{print $3}')      # Return only the tag.

# Craft the URL for the release asset.
version=$(echo $latest | tr -d 'v')  # Remove the leading v.
wheel="airborne-cli-${version}-py3-none-any.whl"
release="${repo}/releases/download/${latest}/${wheel}"

# Install the release.
pip install $release
```

### Building from source

To build the package straight from source, there are two requirements.

1. Python 3.10 and higher
1. Poetry package manager

With that, you can clone or download the repo into you machine, and use
_Poetry_ to install.

```bash
git clone https://github.com/drearondov/airborne-cli.git
cd airborne-cli
poetry install
```

## Usage

Please see the [Command-line Reference] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [GPL 3.0 license][license],
_Airborne CLI_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

- This project is an extension of the wonderful work done by the
  [airborne.cam] team.
- This project was generated from [@cjolowicz]'s
  [Hypermodern Python Cookiecutter] template.

<!-- github-only -->

[@cjolowicz]: https://github.com/cjolowicz
[airborne.cam]: https://airborne.cam
[black]: https://github.com/psf/black
[codecov]: https://app.codecov.io/gh/drearondov/airborne-cli
[command-line reference]: https://airborne-cli.readthedocs.io/en/latest/usage.html
[contributor guide]: https://github.com/drearondov/airborne-cli/blob/main/CONTRIBUTING.md
[file an issue]: https://github.com/drearondov/airborne-cli/issues
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[license]: https://github.com/drearondov/airborne-cli/blob/master/LICENSE
[pre-commit]: https://github.com/pre-commit/pre-commit
[pypi]: https://pypi.org
[python version]: https://pypi.org/project/airborne-cli
[tests]: https://github.com/drearondov/airborne-cli/actions?workflow=Tests
