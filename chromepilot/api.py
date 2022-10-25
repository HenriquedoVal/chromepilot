import os
import sys
import zipfile
from io import BytesIO
from urllib.request import urlopen

from .__init__ import INSTALL_PATH
from . import local


URL = 'https://chromedriver.storage.googleapis.com/'


def get_newer_version_info() -> str:
    r = urlopen(
        URL + 'LATEST_RELEASE'
    )
    return r.read().decode()


def download_newer_version() -> str:

    version = get_newer_version_info()
    if version in local.get_installed_chromedrivers():
        return 'Latest chromedriver is installed.'

    plat = sys.platform
    if plat == 'linux':
        plat += '64'

    version += '/'
    file = urlopen(
        URL + version + f'chromedriver_{plat}.zip'
    )

    bio = BytesIO(file.read())
    zip_handler = zipfile.ZipFile(bio)
    if (err := zip_handler.testzip()) is None:

        download_path = os.path.join(INSTALL_PATH, version) + os.path.sep
        os.mkdir(download_path)

        driver = zip_handler.open('chromedriver.exe')
        content = driver.read()
        with open(download_path + 'chromedriver.exe', 'wb') as out:
            out.write(content)

        return "Download was successful"

    return f"Error on testzip. File: {err}"
