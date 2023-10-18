# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from datetime import datetime

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Airborne CLI"
author = "Andrea Rondon"
copyright = f"{datetime.now().year}, {author}"
release = "1.0.0a0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = []

language = "en"

autodoc_typehints = "description"

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "substitution",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_logo = "_static/logo.png"
html_static_path = ["_static"]
