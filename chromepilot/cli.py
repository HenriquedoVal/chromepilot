import argparse

from . import local
from . import api
from . import utils


def main():
    parser = argparse.ArgumentParser(
        prog='chromepilot',
        description='Chromedriver download manager and shorcuts for Selenium.',
    )

    subparsers = parser.add_subparsers(dest='command', metavar='')
    subparsers.add_parser(
        'search',
        help='Searches for installs of Google Chrome locally.'
    )
    subparsers.add_parser(
        'check',
        help='Checks the version of Google Chrome and chromedrivers.'
    )

    upgrade = subparsers.add_parser(
        'upgrade',
        help=("Download newer versions of chromedriver. "
              "'upgrade -c' cleans after install.")
    )
    upgrade.add_argument(
        '-c',
        const=1,
        action='store_const'
    )

    subparsers.add_parser(
        'clean',
        help='Searches for outdated chromedrivers locally.'
    )
    args = parser.parse_args()

    if args.command == 'search':
        search = local.search_chrome_installed()
        chromes = len(search)
        s = 's' if chromes > 1 else ''
        print(f'{chromes}{s} could be found.')
        if chromes:
            print('Version:')
        for version in search:
            print(version)

    elif args.command == 'check':
        search = local.search_chrome_installed()
        chromedrivers = local.get_installed_chromedrivers()

        newer_chrome = utils.get_newer_version(search)
        newer_local_chromedriver = utils.get_newer_version(chromedrivers)

        newer_online_chromedriver = api.get_newer_version_info()

        print(
            f'Installs of Google Chrome found: {len(search)}.',
            f'Newer local Google Chrome version found: {newer_chrome}',
            f'Installed chromedrivers: {len(chromedrivers)}.',
            f'Newer local chromedriver: {newer_local_chromedriver}',
            f'Newer chromedriver available online: {newer_online_chromedriver}',  # noqa: E501
            sep='\n'
        )

    elif args.command == 'upgrade':
        newer_online_chromedriver = api.get_newer_version_info()
        chromedrivers = local.get_installed_chromedrivers()
        newer_local_chromedriver = utils.get_newer_version(chromedrivers)

        if utils.is_x_newer_than_y(
            newer_online_chromedriver, newer_local_chromedriver
        ):
            print('A new chromedriver is available online.',
                  'Consider upgrading Google Chrome before '
                  'downloading the chromedriver.',
                  sep='\n')
            answer = input('Install latest chromedriver? [y/N]: ')
            if answer.lower() in ('y', 'yes'):
                print(api.download_newer_version())
                if args.c is not None:
                    local.remove_outdated()
                    print('Cleaned older versions.')
        else:
            print('Everything is up to date.')

    elif args.command == 'clean':
        chromedrivers = local.get_installed_chromedrivers()
        if len(chromedrivers) > 1:
            print('Found more than one chromedriver.')
            answer = input('Delete outdated? [y/N]: ')
            if answer.lower() in ('y', 'yes'):
                local.remove_outdated()
                print('Cleaned older versions.')
        else:
            print('Everything clean.')

    elif args.command is None:
        parser.print_help()
        print()
        print(
            'In your runtime, try:',
            '',
            'from chromepilot import short',
            'driver = short.driver()  '
            '# Easy access to pre-configured driver',
            sep='\n'
        )
