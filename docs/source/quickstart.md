# Quickstart

This page gives a quick overview on how to get started with Airborne CLI and
how to use it.

## 1. Install the package

> Note: This package is still under development, and as such it has not been
> published to \[PyPI\]. Also, because of the nature of the package I haven't
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

## 2. Prepare your document

There are three input formats supported, Excel, CSV, and JSON.
