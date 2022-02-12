import re

import click
import socket
import argparse
import sys
import httpc_methods

from click import UsageError

# Helper class to have mutually exclusive options -d and -f
class MutuallyExclusiveOption(click.Option):
    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop('mutually_exclusive', []))
        help = kwargs.get('help', '')
        if self.mutually_exclusive:
            ex_str = ', '.join(self.mutually_exclusive)
            kwargs['help'] = help + (
                    ' NOTE: This argument is mutually exclusive with '
                    ' arguments: [' + ex_str + '].'
            )
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "arguments `{}`.".format(
                    self.name,
                    ', '.join(self.mutually_exclusive)
                )
            )

        return super(MutuallyExclusiveOption, self).handle_parse_result(
            ctx,
            opts,
            args
        )




@click.command()
@click.argument('getpost', required=True)
@click.option('-v', is_flag=True, help="Enables a verbose output from the command-line.")
@click.option('-h', multiple=True, help="Set the header of the request in the format 'key: value.'")
@click.option('-d', cls=MutuallyExclusiveOption,
              help="Associates the body of the HTTP Request with inline data from the command line.",
              mutually_exclusive=["d"])
@click.option('-f', cls=MutuallyExclusiveOption,
              help="Associates the body of the HTTP Request with the data from a given file.",
              mutually_exclusive=["f"])
@click.argument('URL', required=True)
def run_client(v, h, d, f, getpost, url):
    """
    Runs the httpc client.

    GETPOST: Executes the get or post HTTP methods respectively as specified.
    URL: determines the targeted HTTP server.
    """
    matcher = re.search(httpc_methods.URL_REGEX, url)
    host = matcher.group(5)
    port = matcher.group(7)
    path = matcher.group(8)

    if (getpost.upper() == "GET"):
        method = "GET"
        if f is not None or d is not None:
            click.echo("Cannot have data or file for GET method.")
            exit()
    elif (getpost.upper() == "POST"):
        method = "POST"
        if f is None and d is None:
            click.echo("Must have either data or file for POST method.")
            exit()
        elif f is not None and d is not None:
            click.echo("Cannot have both data and file for POST method.")
            exit()
    else:
        click.echo("Invalid query. Must specify GET or POST.")

    for i in range(len(h)):
        if ':' not in h[i]:
            click.echo("Invalid header argument entered.")
            exit()

    requester = httpc_methods.build_request(v, h, d, f, method, host, port, path)
    final_output = httpc_methods.process_request(v, h, d, f, method, host, port, path, requester)

    click.echo(final_output)


if __name__ == '__main__':
    run_client()
