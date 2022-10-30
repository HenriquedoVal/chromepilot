import argparse

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

    subparsers.add_parser(
        'write',
        help='Writes "pilot.toml" template on current directory'
    )

    args = parser.parse_args()

    options = {
        'search': utils.search,
        'check': utils.check,
        'upgrade': utils.upgrade,
        'clean': utils.clean,
        'write': utils.write
    }

    if args.command is None:
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

    else:
        selected = options[args.command]
        if args.command == 'upgrade' and args.c is not None:
            selected(quiet=True)
        else:
            selected()
