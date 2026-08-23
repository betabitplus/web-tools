"""Extract, download, and cache allowed media
==========================================

Take a post-like payload, extract its media URL, download only an allowed image,
and make the cache hit on the repeated download visible.
"""
# sphinx_gallery_tags = ["media", "download", "cache", "policy"]
# sphinx_gallery_thumbnail_path = "_static/gallery/media-download.svg"

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import matplotlib.pyplot as plt
from PIL import Image

from web_tools import MediaConfig, MediaDownloader, MediaItem, MediaType

POST: dict[str, Any] = {
    "url": "https://www.python.org/static/community_logos/python-logo.png",
}


# %%
# Make the download policy explicit
# ---------------------------------
# The downloader receives ordinary public config. This example allows images and
# enables media caching while leaving unrelated media types out of scope.
CONFIG = MediaConfig(
    enabled=True,
    allowed_types=(MediaType.IMAGE,),
    cache_media=True,
    max_downloads_per_post=1,
    use_proxy_for_small=False,
)


# %%
# Extract from the payload, then download through the policy
# ----------------------------------------------------------
def download_twice(cache_dir: Path) -> tuple[list[str], MediaItem, MediaItem]:
    """Download the post image once, then request the same URL from cache."""
    with MediaDownloader(config=CONFIG, cache_dir=cache_dir) as media:
        candidates = media.extract_media_urls(POST)
        items = media.download_from_post(POST)
        if not candidates or not items:
            msg = "Expected media candidate was not downloaded."
            raise RuntimeError(msg)

        second = media.download(candidates[0])
        if second is None:
            msg = "Expected cached media item was not returned."
            raise RuntimeError(msg)
        return candidates, items[0], second


# %%
# Inspect the download and the reused artifact
# --------------------------------------------
# The first item contains the real downloaded bytes; the second makes cache reuse
# explicit through the same public ``MediaItem`` contract.
if __name__ == "__main__":
    with TemporaryDirectory(prefix="web-tools-media-") as temp_dir:
        candidates, first, second = download_twice(Path(temp_dir))

    print(f"candidate:    {candidates[0]}")
    print(f"first:        {first.content_type}, from_cache={first.from_cache}")
    print(f"second:       {second.content_type}, from_cache={second.from_cache}")

    with Image.open(BytesIO(first.content)) as source_image:
        image = source_image.convert("RGBA").copy()

    plt.figure(figsize=(8, 3))
    plt.imshow(image)
    plt.axis("off")
    plt.title("Downloaded media")
    plt.tight_layout()

# %%
# The visible image is the exact downloaded artifact; policy and cache evidence stay
# available alongside the bytes instead of being hidden inside downloader internals.
