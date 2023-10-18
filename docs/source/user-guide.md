# User Guide

This is the user guide for the [Airborne CLI] project, a CLI tool to use the
[airborne.cam] app to analyse several rooms at once.

If you are in a hurry, checkout the [quickstart guide] and the [tutorials].

## Introduction

### About this project

_Airborne CLI_ is a project born during the COVID pandemic, out of the need
to use the [airborne.cam] application to analyse several rooms at once
without having to manually input the data and refresh the page
over an over again.

### Features

- Support to process data in a `.xlsx`, `.csv` or `.json` format (input/output)
- Fully configurable default mode for fast running
- Fully configurable running parameters such as:
  - Maxmimun risk considered,
  - Type of mask used un room
  - Percentage of people infected
  - Viral load (mild, medium, conservative)
  - Maxmimun size of particles considered aerosol
- Exports graphics in `png` and `jpg` format for risk analysis.
- Analysis dashboard per room (comming soon)

## Installation

### Requirements

To be able to us this package, you need a working python instalation with
Python 3.10 or higher and pip.

In case you want to build from source, you will also need to have [Poetry]
installed.

### Package instalation

If you still would like to use this tools, you can get the latest version of
_Airborne CLI_ following this steps.

```bash
repo="https://github.com/drearondov/airborne-cli"

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

You can clone or download the repo into you machine, and use
[Poetry] to install.

```bash
git clone https://github.com/drearondov/airborne-cli.git
cd airborne-cli
poetry install
```

## Preparing the data for processing

In order to be able to process the data, the following fields need to be
present:

- Area
- Height
- 100% occupation
- Activity level
- Time of permanence

## Data processing

During data processing, there are three main aspects being calculated:

- Required ACH calculations for a set maximum risk
- Required ventilation required in the room according to ASHRAE 62.1
- Variation in risk for different parameters

## Results

There are three major results that can be obtained:

- 

[Poetry]: https://python-poetry.org
[Airborne CLI]: https://github.com/drearondov/airborne-cli
[airborne.cam]: https://airborne.cam
