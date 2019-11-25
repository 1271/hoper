from argparse import ArgumentParser, MetavarTypeHelpFormatter
from .meta import version


class Formatter(MetavarTypeHelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            metavar, = self._metavar_formatter(action, default)(1)
            return metavar
        else:
            parts = []
            if action.nargs == 0:
                parts.extend(action.option_strings)
            else:
                default = self._get_default_metavar_for_optional(action)
                args_string = self._format_args(action, default)
                args_len = len(action.option_strings) - 1
                for i, option_string in enumerate(action.option_strings):
                    if i == args_len:
                        parts.append('%s %s' % (option_string, args_string))
                    else:
                        parts.append(option_string)
            return ', '.join(parts)


def get_cli_arguments() -> ArgumentParser:  # pragma: no cover
    args_parser = ArgumentParser(formatter_class=Formatter)

    args_parser.add_argument('url', metavar='url', type=str, help='Analyzed url')
    args_parser.add_argument('-u', '--user-agent', type=str, metavar='AGENT', help='User-agent',
                             default='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                     ' Chrome/51.0.2704.103 Safari/537.36')
    args_parser.add_argument('-c', '--cookies', metavar='COOKIE', type=str, nargs='*', default=[],
                             help='Cookies. Format: --cookies key1=value1 key2=value2')
    args_parser.add_argument('-i', '--show-ip', action='store_true', help='Show ip for each hoop')
    args_parser.add_argument('-v', '--version', action='version', help='Show version and exit', version=version)

    return args_parser


arguments = get_cli_arguments()

__all__ = ['arguments']
