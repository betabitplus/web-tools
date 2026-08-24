"""Sphinx configuration for web-tools documentation."""

from __future__ import annotations

import os

project = "web-tools"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx_gallery.gen_gallery",
    "sphinxcontrib.mermaid",
]

root_doc = "index"
exclude_patterns = ["_build", "README.md"]
myst_fence_as_directive = {"mermaid"}
html_theme = "pydata_sphinx_theme"

# Required CI stays fully offline. Explicit live documentation builds can opt in
# to external inventories for APIs used directly by public examples.
intersphinx_mapping = {}
if os.getenv("SPHINX_ENABLE_INTERSPHINX") == "1":
    intersphinx_mapping = {
        "python": ("https://docs.python.org/3/", None),
        "pillow": ("https://pillow.readthedocs.io/en/stable/", None),
    }

sphinx_gallery_conf = {
    "examples_dirs": "../examples/web_tools",
    "gallery_dirs": "auto_examples",
    "filename_pattern": r".*\.py$",
    "backreferences_dir": "generated/backreferences",
    "doc_module": ("web_tools",),
    "reference_url": {"web_tools": None},
    "junit": "../test-results/sphinx-gallery/junit.xml",
    "remove_config_comments": True,
}
