import re

import click
import httpc_methods

@click.command()
@click.argument('getpost', required=True)
@click.option('-v', is_flag=True, help="Enables a verbose output from the command-line.")
@click.option('-h', multiple=True, help="Set the header of the request in the format 'key: value.'")
@click.option('-d', help="Associates the body of the HTTP Request with inline data from the command line.")
@click.option('-f', help="Associates the body of the HTTP Request with the data from a given file.")
@click.option('-o', help="Write the body of the response to the specified file.")
@click.argument('URL', required=True)
def run_client(v, h, d, f, getpost, url):
    """
    Runs the httpc client.

    GETPOST: Executes the get or post HTTP methods respectively as specified.
    URL: determines the targeted HTTP server.
    """

    if url[0] == "\"" and url[1] == "\"":
        url = url[1:-1]
    elif url[0] == "\'" and url[1] == "\'":
        url = url[1:-1]

    matcher = re.search(httpc_methods.URL_REGEX, url)
    host = matcher.group(5)
    port = matcher.group(7)
    path = matcher.group(8)

    if port is None:
        port = 80
    else:
        port = int(port)

    if path is None or path == "":
        path = "/"
    else:
        path = path

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
