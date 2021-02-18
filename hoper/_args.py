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
    args_parser.add_argument('-c', '--cookies', metavar='C', type=str, nargs='*', default=[],
                             help='Cookies. Format: --cookies key1=value1 key2=value2')
    args_parser.add_argument('-i', '--show-ip', action='store_true', help='Show ip for each hop')
    args_parser.add_argument('-l', '--last-only', action='store_true', help='Show only last url (without history)')
    args_parser.add_argument('-T', '--timeout', type=int, help='How long to wait for te server to send'
                                                               ' data before giving up. In milliseconds (1/100 sec)')
    args_parser.add_argument('-t', '--show-request-time', action='store_true', help='Show request time for each hop')
    args_parser.add_argument('-E', '--no-error-messages', action='store_true', help='Don\'t show error messages')
    args_parser.add_argument('-S', '--no-statistic', action='store_true', help='Don\'t show statistic message')
    # args_parser.add_argument('-p', '--post', action='store_true', help='Use post instead of get')
    args_parser.add_argument('-C', '--count-only', action='store_true', help='Show count hops and exit')
    args_parser.add_argument('-j', '--allow-js-redirects', action='store_true', dest='try_js',
                             help='Try detect js redirects')
    args_parser.add_argument('--proxy', type=str, metavar='URL', nargs='*',
                             help='Proxy. Format: http://proxy:123 (for http and https) or http=http://proxy:123'
                                  ' https=http://secured-proxy:321 ftp=http://ftp-proxy:332')
    args_parser.add_argument('-F', '--do-not-follow-loops', action='store_true', dest='disallow_loops',
                             help='If loop detected, stop operation')
    args_parser.add_argument('-J', '--print-json', action='store_true', help='Print result as json')
    args_parser.add_argument('--pretty-json', action='store_true',
                             help='Makes sense only if the  --print-json argument is specified')
    args_parser.add_argument('-v', '--version', action='version', help='Show version and exit', version=version)
    args_parser.add_argument('-H', '--disallow-hooks', action='store_true', help='Disable special hooks for some sites')

    return args_parser


arguments = get_cli_arguments()

__all__ = ['arguments']
