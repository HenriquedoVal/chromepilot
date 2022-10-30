import shutil
import os
from pathlib import Path

from . import local
from . import api


def search():
    search = local.search_chrome_installed()
    chromes = len(search)
    s = 's' if chromes > 1 else ''
    print(f'{chromes} install{s} could be found.')
    if chromes:
        print('Version:')
    for version in search:
        print(version)


def check():
    search = local.search_chrome_installed()
    chromedrivers = local.get_installed_chromedrivers()

    newer_chrome = get_newer_version(search)
    newer_local_chromedriver = get_newer_version(chromedrivers)

    newer_online_chromedriver = api.get_newer_version_info()

    print(
        f'Installs of Google Chrome found: {len(search)}.',
        f'Newer local Google Chrome version found: {newer_chrome}',
        f'Installed chromedrivers: {len(chromedrivers)}.',
        f'Newer local chromedriver: {newer_local_chromedriver}',
        f'Newer chromedriver available online: {newer_online_chromedriver}',
        sep='\n'
    )


def upgrade():
    if upgrade_available():
        print('A new chromedriver is available online.',
              'Consider upgrading Google Chrome before '
              'downloading the chromedriver.',
              sep='\n')
        answer = input('Install latest chromedriver? [y/N]: ')
        if answer.lower() in ('y', 'yes'):
            print(api.download_newer_version())
    else:
        print('Everything is up to date.')


def upgrade_available():
    newer_online_chromedriver = api.get_newer_version_info()
    chromedrivers = local.get_installed_chromedrivers()
    newer_local_chromedriver = get_newer_version(chromedrivers)

    return is_x_newer_than_y(
        newer_online_chromedriver, newer_local_chromedriver
    )


def clean(quiet: bool = False):
    if quiet:
        return local.remove_outdated()
    chromedrivers = local.get_installed_chromedrivers()
    if len(chromedrivers) > 1:
        print('Found more than one chromedriver.')
        answer = input('Delete outdated? [y/N]: ')
        if answer.lower() in ('y', 'yes'):
            local.remove_outdated()
            print('Cleaned older versions.')
    else:
        print('Everything clean.')


def write():
    if not os.path.exists('pilot.toml'):
        shutil.copy(Path(local.__file__).parent / 'pilot.toml', '.')
    else:
        print("There's already a \"pilot.toml\" in current directory.")


def get_newer_version(versions: list[str]) -> str:
    versions.sort(
        key=lambda x: (x.split('.')[0],
                       x.split('.')[2],
                       x.split('.')[3]),
        reverse=True
    )

    if len(versions) > 0:
        return versions[0]


def is_x_newer_than_y(x: str, y: str) -> bool:
    if y is None:
        return True

    x = [int(i) for i in x.split('.')]
    y = [int(i) for i in y.split('.')]
    for ind in (0, 2, 3):
        if x[ind] > y[ind]:
            return True
    return False
