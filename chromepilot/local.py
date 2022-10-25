import os
from pathlib import Path

from .__init__ import INSTALL_PATH


usual = 'Google\\Chrome\\Application'
X86_PATH = os.path.join(
    os.environ.get('HOMEDRIVE', 'NONE') + '\\',
    'Program Files (x86)',
    usual,
    'chrome.exe'
)

LOCALAPPDATA_PATH = os.path.join(
    os.environ.get('LOCALAPPDATA', 'NONE'),
    usual,
    'chrome.exe'
)

ALL_SEARCH_PATHS = [
    X86_PATH,
    LOCALAPPDATA_PATH
]


def search_chrome_installed() -> str:
    import re

    valid_paths = []
    for path in ALL_SEARCH_PATHS:
        if os.path.exists(Path(path).resolve()):
            valid_paths.append(path)

    valid_paths = [i.removesuffix('chrome.exe') for i in valid_paths]

    versions = []
    for path in valid_paths:
        for out in os.listdir(path):
            if m := re.match('[0-9]+.0.[0-9]+.[0-9]+', out):
                versions.append(m.string)

    return versions


def get_installed_chromedrivers() -> list:
    return [i for i in os.listdir(INSTALL_PATH)]


def remove_outdated() -> None:
    from .utils import get_newer_version

    chromedrivers = get_installed_chromedrivers()
    newer = get_newer_version(chromedrivers)
    chromedrivers.remove(newer)

    for directory in chromedrivers:
        os.remove(
            os.path.join(
                INSTALL_PATH,
                directory,
                'chromedriver.exe'
            )
        )
        os.rmdir(
            os.path.join(
                INSTALL_PATH,
                directory
            )
        )
