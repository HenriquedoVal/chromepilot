# Chromepilot
### Chromedriver download manager and imports shortcuts

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
    upgrade   Download newer versions of chromedriver. 'upgrade -c' cleans after install.
    clean     Searches for outdated chromedrivers locally.
    write     Writes "pilot.toml" template on current directory

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
>>>
>>> driver = short.driver()
>>> driver.get('some/url')
>>> entity = driver.find_element(short.By.TAG_NAME, 'tag')
~~~

The _pilot.toml_ is a file where you define the config for your driver and
the shortcuts for Selenium (your most used imports).  
  
When you import `chromepilot.short` it will search for a 'global' _pilot.toml_  
in `~/.cache/chromepilot` in linux and `%LOCALAPPDATA%\chromepilot` in Windows.  
This file will be readden wherever you import `chromepilot.short`.  
  
The settings for the global _pilot.toml_ will be overwritten by a 'local' one,  
that is, the _pilot.toml_ in the same directory as your `main.py`.  
  
Just do a `chromepilot write` to see how the _pilot.toml_ looks like.  
  

## Moreover
~~~Python
>>> short.global_toml  # Has chromepilot parsed my global pilot.toml?
True

>>> short.local_toml  # Has chromepilot parsed my local pilot.toml?
True

>>> short.parsed_options  # dict containing the values passed to driver constructor
{'service': {...}, ...}

>>> driver = short.driver(use_toml=False)  # Don't use toml
~~~

p.s: There's no dependencies for the CLI usage.
     If your Python version is below 3.11 you will need the `tomlkit` package to use `chromepilot.short`.
     Selenium is a dependency if you want `short.driver()`
