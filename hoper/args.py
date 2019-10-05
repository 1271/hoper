from argparse import ArgumentParser
from .meta import version


def get_cli_arguments() -> ArgumentParser:  # pragma: no cover
    args_parser = ArgumentParser()

    args_parser.add_argument('url', metavar='url', type=str, help='Downloaded url')
    args_parser.add_argument('-u', '--user-agent', type=str, help='User-agent', default='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
    args_parser.add_argument('-v', '--version', action='version', help='Show version and exit', version=version)

    return args_parser


arguments = get_cli_arguments()

__all__ = ['arguments']
