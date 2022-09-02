"""Sphinx configuration."""
project = "Airborne CLI"
author = "Andrea Rondón"
copyright = "2022, Andrea Rondón"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
