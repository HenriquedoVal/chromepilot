# Chromepilot. Chromedriver download manager and shortcuts for Selenium.

Description:  
Download, unzip in memory and manages chromedrivers.
Easily integrates with Selenium webdriver.

## Installation
~~~
> pip install chromepilot
~~~

## CLI
~~~
usage: chromepilot [-h]  ...

Chromedriver download manager and shorcuts for Selenium.

positional arguments:
  
    search    Searches for installs of Google Chrome locally.
    check     Checks the version of Google Chrome and chromedrivers.
    upgrade   Download newer versions of chromedriver online.
    clean     Searches for outdated chromedrivers locally.

options:
  -h, --help  show this help message and exit

In your runtime, try:

from chromepilot import short
driver = short.driver()  # Easy access to pre-configured driver
~~~

## Runtime
~~~Python
>>> # After install whith `> chromepilot upgrade`
>>> from chromepilot import short
>>> driver = short.driver()
>>> driver.get('some/url')
>>> entity = driver.find_element(short.By.TAG_NAME, 'tag')
~~~

TODO:
- parse user configs to create webdriver
- parse user configs to create shortcuts
