# py-kraken
A python module to download files from KrakenFiles

## Install
`pip install py-kraken`

## Command Line Use
`kraken-download https://krakenfiles.com/view/dbe8ee9c34/file.html`

## Module Use
```python
from pykraken import Kraken

kraken_link = "https://krakenfiles.com/view/dbe8ee9c34/file.html"

# Download the file to local directory
k = Kraken()
k.download_file(kraken_link)

# Convert the kraken link to a download link
download_link = k.get_download_link(kraken_link)

print(download_link)

# 'https://krakenfiles.com/force-download/YXNkejUzNERTZmRzU0RGY3YzMmRiZThlZTljMzR8MTYxNTA3MDkyNA?fileHash=dbe8ee9c34'
