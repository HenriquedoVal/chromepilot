import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Expose import as shortcuts
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

from .__init__ import INSTALL_PATH
from .local import get_installed_chromedrivers
from .utils import get_newer_version

__all__ = ['By', 'WebDriverException', 'Keys', 'driver']


def driver():
    chromedrivers = get_installed_chromedrivers()
    if not chromedrivers:
        return
    newer_chromedriver = get_newer_version(chromedrivers)

    path = os.path.join(INSTALL_PATH, newer_chromedriver)
    path += os.path.sep + 'chromedriver.exe'

    service = Service(
            executable_path=path,
            log_path=os.devnull
        )
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument('disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(2)

    return driver
