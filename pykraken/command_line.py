"""Command-line interface for downloading files from KrakenFiles."""

import argparse

from .kraken import Kraken


def kraken_download(path: str):
    """Download a file from a KrakenFiles URL to the current directory.

    Args:
        path: The KrakenFiles page URL to download from.
    """
    k = Kraken()
    k.download_file(path)


def main():
    """Entry point for the ``kraken-download`` CLI command.

    Parses command-line arguments and downloads the file specified by the
    given KrakenFiles URL.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="path help")
    args = parser.parse_args()
    kraken_download(args.path)


if __name__ == "__main__":
    main()
