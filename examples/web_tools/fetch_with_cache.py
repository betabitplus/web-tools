"""Fetch a page and reuse the cached artifact
==========================================

Fetch one live page twice through the public page cache and use ``from_cache``
to see whether the HTML came from the network-facing workflow or local storage.
"""
# sphinx_gallery_tags = ["fetch", "cache", "async"]
# sphinx_gallery_thumbnail_path = "_static/gallery/fetch-cache.svg"

from __future__ import annotations

import asyncio
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from web_tools import FetchResponse, configure_cache, fetch_html

PAGE_URL = "https://example.com/"


# %%
# Isolate the example cache
# -------------------------
# A temporary directory keeps this run independent from any cache the caller may
# already use. ``configure_cache(None)`` restores the default afterwards.
async def fetch_twice(cache_dir: Path) -> tuple[FetchResponse, FetchResponse]:
    """Fetch one URL twice through a fresh public page cache."""
    configure_cache(cache_dir)
    try:
        with redirect_stderr(StringIO()):
            first = await fetch_html(PAGE_URL)
            second = await fetch_html(PAGE_URL)
    finally:
        configure_cache(None)
    return first, second


# %%
# Fetch twice and inspect cache evidence
# --------------------------------------
# The request API is identical both times; the response tells the caller where the
# second artifact came from.
if __name__ == "__main__":
    with TemporaryDirectory(prefix="web-tools-cache-") as temp_dir:
        first, second = asyncio.run(fetch_twice(Path(temp_dir)))

    print(f"first fetch:  from_cache={first.from_cache}")
    print(f"second fetch: from_cache={second.from_cache}")
    print(f"same page:    {first.html == second.html}")
    print(f"content:      {'Example Domain' in second.html}")

# %%
# The second response reuses the cached page artifact without changing the public
# ``fetch_html()`` call or hiding that fact from the caller.
