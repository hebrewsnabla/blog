# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'quoi'
copyright = '2021, wsr'
author = 'wsr'

# The full version, including alpha/beta/rc tags
#release = '0.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
#    'recommonmark', 
    'sphinx.ext.mathjax',
    'sphinxcontrib.bibtex',
    'myst_parser',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


master_doc = 'index'
source_suffix = {
    '.rst': 'restructuredtext',
#    '.md': 'markdown',
}
#source_parsers = {
#    '.md': CommonMarkParser,
#    '.MD': CommonMarkParser,
#}
bibtex_bibfiles = [
    'refs.bib'
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_book_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_theme_options = {
    "repository_url": "https://github.com/hebrewsnabla/blog",
    "use_repository_button": True,
    "use_issues_button": True,
#    "toc_title": "文档目录",
}
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_image",
]

def setup(app):
    app.add_config_value('recommonmark_config', {
            'enable_math': True,
            'enable_inline_math': True,
            }, True)
#    app.add_transform(AutoStructify)
#mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
    # https://stackoverflow.com/questions/23211695/modifying-content-width-of-the-sphinx-theme-read-the-docs
    app.add_css_file('custom.css')

