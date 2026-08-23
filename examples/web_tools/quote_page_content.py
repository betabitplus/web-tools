"""Turn page content into screenshot evidence
==========================================

Find ordinary text and a converted visual element on a live page, then inspect
the annotated screenshots returned by the public quoting API.
"""
# sphinx_gallery_tags = ["quote", "screenshot", "browser", "manifest"]
# sphinx_gallery_thumbnail_path = "_static/gallery/quoting.svg"

from __future__ import annotations

import asyncio
from contextlib import redirect_stderr
from io import StringIO

import matplotlib.pyplot as plt

from web_tools import (
    QuoteMatch,
    VisualElementMatch,
    VisualElementType,
    fetch_html,
    html2md,
    quote_element,
    quote_text,
)

PAGE_URL = "https://w3schoolsua.github.io/html/html_tables_en.html"
TARGET_TEXT = "HTML tables allow web developers to arrange data into rows and columns."


# %%
# Derive a public table ID from the same page
# -------------------------------------------
# Conversion assigns IDs such as ``T_0``. Quoting accepts that public ID directly,
# so callers never need a CSS selector or browser handle.
async def collect_evidence() -> tuple[QuoteMatch, VisualElementMatch]:
    """Return text and table screenshot evidence from one live page."""
    with redirect_stderr(StringIO()):
        page = await fetch_html(PAGE_URL, force_refresh=True)
        converted = html2md(page.html, base_url=page.url)
        table = next(
            element
            for element in converted.manifest.elements
            if element.element_type == VisualElementType.TABLE
        )

        text_matches = await quote_text(TARGET_TEXT, page.url, force_refresh=True)
        table_match = await quote_element(table.id, page.url)
    if not text_matches or table_match is None:
        msg = "Expected live quote evidence was not found."
        raise RuntimeError(msg)
    return text_matches[0], table_match


# %%
# Quote the content and inspect semantic evidence
# -----------------------------------------------
# Both calls return caller-facing DTOs containing the match metadata and an
# annotated Pillow image.
if __name__ == "__main__":
    text_match, table_match = asyncio.run(collect_evidence())

    print(f"text:  {text_match.text!r}")
    print(f"boxes: {len(text_match.boxes)}")
    print(f"table: {table_match.id} ({table_match.element_type.value})")

    plt.figure(figsize=(10, 6))
    plt.imshow(text_match.image)
    plt.axis("off")
    plt.title("Text quote")
    plt.tight_layout()

    plt.figure(figsize=(10, 6))
    plt.imshow(table_match.image)
    plt.axis("off")
    plt.title(f"Visual element {table_match.id}")
    plt.tight_layout()

# %%
# The screenshots are the result: the package locates and annotates the requested
# page content while the caller stays entirely on stable public IDs and DTOs.
