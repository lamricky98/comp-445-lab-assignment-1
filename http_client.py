import click
import socket
import argparse
import sys

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


POST = "POST"
GET = "GET"
URL_REGEX = "((http[s]?|ftp):\/)?\/?((www\.)?([^:\/\s\?]+))(:(\d+))?(((\/[\w\/]*)?(\.\w+))?(\?([\w=&]+))?)"
blank_line = '\r\n'
path = "/"
port = 80
contentType = "Content-Type: {content_type}"
contentLength = "Content-length: {content_length}"

@click.command()
@click.option('get', is_flag=True, cls=MutuallyExclusiveOption,
              help="Executes the HTTP GET method.",
              mutually_exclusive=["post"])
@click.option('post', is_flag=True, cls=MutuallyExclusiveOption,
              help="Executes the HTTP POST method.",
              mutually_exclusive=["get"])
@click.option('-v', is_flag=True, help="Enables a verbose output from the command-line.")
@click.option('-h', multiple=True, help="Set the header of the request in the format 'key: value.'")
@click.option('-d', cls=MutuallyExclusiveOption,
              help="Associates the body of the HTTP Request with inline data from the command line.",
              mutually_exclusive=["d"])
@click.option('-f', cls=MutuallyExclusiveOption,
              help="Associates the body of the HTTP Request with the data from a given file.",
              mutually_exclusive=["f"])
@click.argument('URL')
def run_client(v, h, d, f, get, post):
    """
    Runs the httpc client.

    URL: determines the targeted HTTP server.
    """
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((host, port))
        print("Type any thing then ENTER. Press Ctrl+C to terminate")
        while True:
            line = sys.stdin.readline(1024)
            request = line.encode("utf-8")
            conn.sendall(request)
            # MSG_WAITALL waits for full request or error
            response = conn.recv(len(request), socket.MSG_WAITALL)
            sys.stdout.write("Replied: " + response.decode("utf-8"))
    finally:
        conn.close()


# Usage: python echoclient.py --host host --port port
parser = argparse.ArgumentParser()
parser.add_argument("--host", help="server host", default="localhost")
parser.add_argument("--port", help="server port", type=int, default=8007)
args = parser.parse_args()
run_client(args.host, args.port)

if __name__ == '__main__':
    server = HTTPServer()
    server.start()
