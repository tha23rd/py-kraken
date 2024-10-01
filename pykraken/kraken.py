import cgi
import os
import shutil

import requests
from bs4 import BeautifulSoup


class HashNotFoundException(Exception):
    def __init__(self, exception):
        super(exception)


class LinkPostFailure(Exception):
    def __init__(self, exception):
        super(exception)


class Kraken:
    _base_headers = {
        "content-type": "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        "cache-control": "no-cache",
    }

    URL_KEY = "url"

    KRAKEN_BASE_URL = "https://krakenfiles.com"

    def __init__(self, session: requests.Session = requests.session()):
        self.session = session

    def get_download_link(self, page_link: str) -> str:

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
        dl_link = self.get_download_link(page_link)

        with self.session.get(dl_link, headers=self._base_headers, stream=True) as r:
            _, params = cgi.parse_header(r.headers["content-disposition"])
            fname = params["filename"]
            with open(os.path.join(path, fname), "wb") as f:
                shutil.copyfileobj(r.raw, f)

            return os.path.join(path, fname)
