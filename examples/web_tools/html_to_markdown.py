"""Convert HTML into Markdown and visual IDs
===========================================

Turn caller-provided HTML into readable Markdown while keeping stable IDs for
pictures, tables, and math that can be referenced by later workflows.
"""
# sphinx_gallery_tags = ["html", "markdown", "manifest"]
# sphinx_gallery_thumbnail_path = "_static/gallery/html-conversion.svg"

from __future__ import annotations

from web_tools import html2md

# %%
# Start with ordinary HTML
# ------------------------
# A single image keeps the input small while making both the text output and one
# visual manifest entry visible.
ARTICLE_HTML = """
<article>
  <h1>Quarterly metrics</h1>
  <p>Revenue grew by 18 percent.</p>
  <img src="https://example.com/charts/revenue.png" alt="Revenue chart">
</article>
"""

# %%
# Convert once and inspect both artifacts
# ---------------------------------------
# ``html2md()`` is the core action: one public call returns readable Markdown plus
# a manifest of visual elements.
if __name__ == "__main__":
    response = html2md(ARTICLE_HTML)

    print(response.markdown.strip())
    print("\nvisuals:")
    for element in response.manifest.elements:
        detail = element.src or f"rows={element.row_count}"
        print(f"  {element.id}: {element.element_type.value} ({detail})")

# %%
# The Markdown is ready for text-oriented consumers, while ``P_0`` remains a stable
# public handle for the visual artifact found in the same document.
