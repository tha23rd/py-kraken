"""py-kraken: A Python module to download files from KrakenFiles.

Provides the ``Kraken`` class for resolving KrakenFiles page URLs to direct
download links and downloading files to the local filesystem.

Example::

    from pykraken.kraken import Kraken

    k = Kraken()
    k.download_file("https://krakenfiles.com/view/abc123/file.html")
"""

from . import kraken

__all__ = [
    "kraken",
]
