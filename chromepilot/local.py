import os
import sys
import re
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


def _search_chrome_windows() -> list:
    valid_paths = []
    for path in ALL_SEARCH_PATHS:
        if os.path.exists(path):
            valid_paths.append(path)

    valid_paths = [i.removesuffix('chrome.exe') for i in valid_paths]

    versions = []
    for path in valid_paths:
        for out in os.listdir(path):
            if m := re.match('[0-9]+.0.[0-9]+.[0-9]+', out):
                versions.append(m.string)

    if versions:
        return versions


def _search_chrome_linux() -> list:
    import shutil

    if (bin := shutil.which('google-chrome')) is not None:
        res = os.popen(f'{bin} --version').read()
        return re.findall('[0-9]+.0.[0-9]+.[0-9]+', res)


def search_chrome_installed() -> list:
    if sys.platform == 'win32':
        return _search_chrome_windows()
    elif sys.platform == 'linux':
        return _search_chrome_linux()


def get_installed_chromedrivers() -> list:
    return [i for i in os.listdir(INSTALL_PATH)]


def remove_outdated() -> None:
    from .utils import get_newer_version

    chromedrivers = get_installed_chromedrivers()
    newer = get_newer_version(chromedrivers)
    chromedrivers.remove(newer)

    for directory in chromedrivers:
        os.remove(os.path.join(
            INSTALL_PATH,
            directory,
            'chromedriver.exe'
        ))
        os.rmdir(os.path.join(
            INSTALL_PATH,
            directory
        ))
