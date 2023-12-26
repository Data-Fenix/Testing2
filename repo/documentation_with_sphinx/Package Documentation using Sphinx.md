# Summary - How to generate the documentation
When the documentation docs/source directory has already been setup, you just need to run the following commands to generate the html documentation from the root folder of the repo root directory. `PACKAGE_PATH` refers to the relative path from the root of the repo.

```shell
PACKAGE_PATH=src/pedata #PACKAGE_PATH=src/eep 
sphinx-apidoc -f -o $PACKAGE_PATH/docs/source $PACKAGE_PATH         
sphinx-build -M html $PACKAGE_PATH/docs/source $PACKAGE_PATH/docs/build
chrome $PACKAGE_PATH/docs/build/html/index.html # for linus
open -a "Google Chrome" $PACKAGE_PATH/docs/build/html/index.html # for mac
```

# Creating a HTML documentation for a python package using Sphinx
https://www.sphinx-doc.org/en/master/
## Installation 
### Sphinx
`pip install sphinx`

### Sphinx themes
`pip install renku-sphinx-theme`

## Setting up the docs folder
The docs folder should be in the main/package/folder (containing the __init__.py file) \
- Go to the main package folder: `cd <main/package/folder>` 
- Create the docs folder: `mkdir docs` 
- Go to the docs folder: `cd docs` 

## Initializing a sphinx project
- In the terminal: `sphinx-quickstart`
```
Welcome to the Sphinx 6.2.1 quickstart utility.

Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).

Selected root path: .

You have two options for placing the build directory for Sphinx output.
Either, you use a directory "_build" within the root path, or you separate
"source" and "build" directories within the root path.
> Separate source and build directories (y/n) [n]: y

The project name will occur in several places in the built documentation.
> Project name: eep_documentation
> Author name(s): Exazyme
> Project release []: 2023.10.20.1

If the documents are to be written in a language other than English,
you can select a language here by its language code. Sphinx will then
translate text that it generates into that language.

For a list of supported codes, see
https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-language.
> Project language [en]: 

Creating file /Users/jean/Devel/python/enzyme_efficiency_prediction/src/eep/docs/source/conf.py.
Creating file /Users/jean/Devel/python/enzyme_efficiency_prediction/src/eep/docs/source/index.rst.
Creating file /Users/jean/Devel/python/enzyme_efficiency_prediction/src/eep/docs/Makefile.
Creating file /Users/jean/Devel/python/enzyme_efficiency_prediction/src/eep/docs/make.bat.

Finished: An initial directory structure has been created.
```
- modify the `docs/source/conf.py` file as needed. E.g. the html theme can be changed there
```python
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "eep_documentation"
copyright = "2023, Exazyme"
author = "Exazyme"
release = "2023.10.20.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "renku"

html_static_path = ["_static"]

```
## Add your packages to the sphinx project
- go back in the root folder `cd ..`

- get the python packages `.rst` files inside the source folder `sphinx-apidoc -f -o src/eep/docs/source src/eep` 
- -> not 100% sure about this command, but after this there should be as many `.rst` files in the source folder as there are subpackages in the package (folders with an `__init__.py` file) 

- update the source/index.rst file with the names of the .rst files (modules) which should be included

```rst
.. eep_documentation documentation master file, created by
   sphinx-quickstart on Fri Oct 20 17:50:15 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to eep_documentation's documentation!
=============================================

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   eep
   eep.models
   eep.policies
   eep.engineer
   eep.generate
   eep.utils

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

```

## Build

- run `sphinx-build -M html docs/source docs/build`

The HTLM files should now be in the docs/build/html folder.


## The HTML documentation is ready to be browsed


