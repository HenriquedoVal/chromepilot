import os
import pathlib
try:
    import tomllib
except ImportError:
    import tomlkit as tomllib

from .__init__ import INSTALL_PATH

HOME = pathlib.Path(INSTALL_PATH).parent


def import_as(x: dict[str, str]) -> None:
    for i, j in x.items():
        exec('import %s as %s' % (i, j))
        exec('globals().update({"%s": %s})' % (j, j))


def from_import(x: dict[str, str]) -> None:
    for i, j in x.items():
        exec('from %s import %s' % (i, j))
        exec('globals().update({"%s": %s})' % (j, j))


def from_import_as(x: dict[str, list[str, str]]):
    for i, j in x.items():
        exec('from %s import %s as %s' % (i, j[0], j[1]))
        exec('globals().update({"%s": %s})' % (j[1], j[1]))


def parse_toml(path):
    with open(path, 'rb') as f:
        file = tomllib.load(f)

    imp_as = file.get('import', {}).get('as')
    from_imp = file.get('from', {}).get('import')
    from_imp_as = from_imp.pop('as', None)
    if imp_as is not None:
        import_as(imp_as)
    if from_imp is not None:
        from_import(from_imp)
    if from_imp_as is not None:
        from_import_as(from_imp_as)

    global parsed_options

    service = file.get('service', {})
    add_argument = file.get('add_argument', {})
    experimental = file.get('add_experimental_option', {})
    imp_wait = file.get('implicitly_wait', {})

    if parsed_options:
        parsed_options['service'].update(service)
        parsed_options['add_argument'].update(add_argument)
        parsed_options['experimental'].update(experimental)
        parsed_options['implicitly_wait'].update(imp_wait)
    else:
        parsed_options['service'] = service
        parsed_options['add_argument'] = add_argument
        parsed_options['experimental'] = experimental
        parsed_options['implicitly_wait'] = imp_wait


def driver(use_toml: bool = True):
    import os
    import sys

    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service

    from .__init__ import INSTALL_PATH
    from .local import get_installed_chromedrivers
    from .utils import get_newer_version

    chromedrivers = get_installed_chromedrivers()
    if not chromedrivers:
        return
    newer_chromedriver = get_newer_version(chromedrivers)

    chromedriver = 'chromedriver.exe'
    if sys.platform == 'linux':
        chromedriver = 'chromedriver'

    path = os.path.join(INSTALL_PATH, newer_chromedriver)
    path += os.path.sep + chromedriver

    if use_toml:
        global parsed_options

        service = parsed_options.get('service', {})
        add_argument = parsed_options.get('add_argument', {})
        experimental = parsed_options.get('experimental', {})
        imp_wait = parsed_options.get('implicitly_wait', {})

    else:
        service, add_argument, experimental, imp_wait = {}, {}, {}, {}

    port = service.get('port', 0)
    service_args = service.get('service_args', None)
    log_path = service.get('log_path', None)

    service = Service(
            executable_path=path,
            port=port,
            service_args=service_args,
            log_path=log_path
        )
    options = webdriver.ChromeOptions()

    args = [key for key in add_argument if add_argument[key]]
    for arg in args:
        options.add_argument(arg)

    for arg in experimental:
        options.add_experimental_option(arg, experimental[arg])

    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(imp_wait.get('value', 0))

    return driver


def get_local_toml_path():
    """
    Searches for pilot.toml in the same dir of users main.py
    not os.getcwd()

    """
    import sys

    user_main_file_dir = os.path.abspath(pathlib.Path(sys.argv[0]).parent)
    return os.path.join(user_main_file_dir, 'pilot.toml')


parsed_options = {}

global_toml = os.path.exists(HOME / 'pilot.toml')
if global_toml:
    parse_toml(HOME / 'pilot.toml')

local_toml_path = get_local_toml_path()
local_toml = os.path.exists(local_toml_path)
if local_toml:
    parse_toml(local_toml_path)

del (HOME, INSTALL_PATH, os, tomllib, pathlib,
     parse_toml, import_as, from_import, from_import_as,
     local_toml_path, get_local_toml_path)
