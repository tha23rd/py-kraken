# py-kraken

[![PyPI version](https://img.shields.io/pypi/v/py-kraken)](https://pypi.org/project/py-kraken/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python module to download files from [KrakenFiles](https://krakenfiles.com).

## Installation

```bash
pip install py-kraken
```

Or install from source:

```bash
git clone https://github.com/tha23rd/py-kraken.git
cd py-kraken
pip install .
```

## CLI Usage

Download a file directly from the command line:

```bash
kraken-download https://krakenfiles.com/view/dbe8ee9c34/file.html
```

The file will be saved to the current working directory.

## Module Usage

### Basic Download

```python
from pykraken.kraken import Kraken

k = Kraken()
k.download_file("https://krakenfiles.com/view/dbe8ee9c34/file.html")
```

### Get Download Link Without Downloading

```python
from pykraken.kraken import Kraken

k = Kraken()
download_link = k.get_download_link("https://krakenfiles.com/view/dbe8ee9c34/file.html")
print(download_link)
```

### Download to a Specific Directory

```python
from pykraken.kraken import Kraken

k = Kraken()
saved_path = k.download_file(
    "https://krakenfiles.com/view/dbe8ee9c34/file.html",
    path="/tmp/downloads/"
)
print(f"File saved to: {saved_path}")
```

### Using a Custom Session

```python
import requests
from pykraken.kraken import Kraken

session = requests.Session()
session.headers.update({"User-Agent": "my-app/1.0"})

k = Kraken(session=session)
k.download_file("https://krakenfiles.com/view/dbe8ee9c34/file.html")
```

## API Reference

### `Kraken(session=None)`

Main class for interacting with KrakenFiles.

**Parameters:**
- `session` (`requests.Session`, optional) — A custom requests session. Defaults to a new session.

#### `get_download_link(page_link: str) -> str`

Resolves a KrakenFiles page URL to a direct download link.

**Parameters:**
- `page_link` (`str`) — The KrakenFiles page URL (e.g. `https://krakenfiles.com/view/.../file.html`).

**Returns:** The direct download URL as a string.

**Raises:**
- `HashNotFoundException` — If the file hash cannot be found on the page.
- `LinkPostFailure` — If the download URL cannot be obtained from the API.

#### `download_file(page_link: str, path: str = "./") -> str`

Downloads a file from a KrakenFiles page URL to the local filesystem.

**Parameters:**
- `page_link` (`str`) — The KrakenFiles page URL.
- `path` (`str`, optional) — Directory to save the file. Defaults to `"./"`.

**Returns:** The full path to the downloaded file.

**Raises:**
- `HashNotFoundException` — If the file hash cannot be found on the page.
- `LinkPostFailure` — If the download URL cannot be obtained from the API.

### Exceptions

#### `HashNotFoundException`

Raised when the file hash cannot be extracted from the KrakenFiles page. This typically means the page URL is invalid or the page structure has changed.

#### `LinkPostFailure`

Raised when the KrakenFiles API does not return a download URL. This can happen if the file has been removed or the token has expired.

## Error Handling

```python
from pykraken.kraken import Kraken, HashNotFoundException, LinkPostFailure

k = Kraken()
try:
    k.download_file("https://krakenfiles.com/view/abc123/file.html")
except HashNotFoundException:
    print("Could not find file hash — check that the URL is valid")
except LinkPostFailure:
    print("Failed to get download link — the file may have been removed")
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes
4. Push to the branch and open a Pull Request

## License

[MIT](https://opensource.org/licenses/MIT)
