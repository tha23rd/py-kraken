"""Core module for interacting with the KrakenFiles service."""

import cgi
import os
import shutil

import requests
from bs4 import BeautifulSoup


class HashNotFoundException(Exception):
    """Raised when the file hash cannot be extracted from a KrakenFiles page.

    This typically indicates that the page URL is invalid or the page structure
    has changed.

    Args:
        exception: A description of the error.
    """

    def __init__(self, exception):
        super(exception)


class LinkPostFailure(Exception):
    """Raised when the KrakenFiles API fails to return a download URL.

    This can occur when the file has been removed or the download token has
    expired.

    Args:
        exception: A description of the error.
    """

    def __init__(self, exception):
        super(exception)


class Kraken:
    """Client for downloading files from KrakenFiles.

    Handles page scraping, token extraction, and file download from
    krakenfiles.com URLs.

    Args:
        session: An optional ``requests.Session`` to use for HTTP requests.
            Defaults to a new session.

    Example::

        k = Kraken()
        k.download_file("https://krakenfiles.com/view/abc123/file.html")
    """

    _base_headers = {
        "content-type": "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        "cache-control": "no-cache",
    }

    URL_KEY = "url"

    KRAKEN_BASE_URL = "https://krakenfiles.com"

    def __init__(self, session: requests.Session = requests.session()):
        self.session = session

    def get_download_link(self, page_link: str) -> str:
        """Resolve a KrakenFiles page URL to a direct download link.

        Scrapes the given page for the file hash and download token, then
        posts to the KrakenFiles API to obtain the direct download URL.

        Args:
            page_link: The full KrakenFiles page URL
                (e.g. ``https://krakenfiles.com/view/dbe8ee9c34/file.html``).

        Returns:
            The direct download URL as a string.

        Raises:
            HashNotFoundException: If the file hash cannot be found on the page.
            LinkPostFailure: If the API does not return a download URL.
        """
        page_resp = self.session.get(page_link)
        soup = BeautifulSoup(page_resp.text, "lxml")

        # parse token
        token = soup.find("input", id="dl-token")["value"]

        # attempt to find hash
        hashes = [
            item["data-file-hash"]
            for item in soup.find_all("div", attrs={"data-file-hash": True})
        ]
        if len(hashes) < 1:
            raise HashNotFoundException(f"Hash not found for page_link: {page_link}")

        dl_hash = hashes[0]

        payload = f'------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="token"\r\n\r\n{token}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--'
        headers = {
            **self._base_headers,
            "hash": dl_hash,
        }

        dl_link_resp = self.session.post(
            f"{self.KRAKEN_BASE_URL}/download/{dl_hash}", data=payload, headers=headers
        )
        dl_link_json = dl_link_resp.json()

        if self.URL_KEY in dl_link_json:
            return dl_link_json[self.URL_KEY]
        else:
            raise LinkPostFailure(
                f"Failed to acquire download URL from kraken for page_link: {page_link}"
            )

    def download_file(self, page_link: str, path: str = "./") -> str:
        """Download a file from a KrakenFiles page URL.

        Resolves the page URL to a direct download link, then streams the
        file to the specified local directory.

        Args:
            page_link: The full KrakenFiles page URL.
            path: Local directory to save the downloaded file. Defaults to
                the current working directory.

        Returns:
            The full path to the saved file.

        Raises:
            HashNotFoundException: If the file hash cannot be found on the page.
            LinkPostFailure: If the API does not return a download URL.
        """
        dl_link = self.get_download_link(page_link)

        with self.session.get(dl_link, headers=self._base_headers, stream=True) as r:
            _, params = cgi.parse_header(r.headers["content-disposition"])
            fname = params["filename"]
            with open(os.path.join(path, fname), "wb") as f:
                shutil.copyfileobj(r.raw, f)

            return os.path.join(path, fname)
