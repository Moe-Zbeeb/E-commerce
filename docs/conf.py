import os
import sys
sys.path.insert(0, os.path.abspath('/home/mohammad/E-commerce-1'))  # Adjust the path as needed

extensions = [
    'sphinx.ext.autodoc',             # For auto-generating documentation from docstrings
    'sphinx.ext.napoleon',            # For Google/NumPy style docstrings
    'sphinx.ext.viewcode',            # Links to source code
    'sphinxcontrib.httpdomain',       # For documenting HTTP APIs
    'm2r2',                           # For Markdown support
]

html_theme = 'sphinx_rtd_theme'

