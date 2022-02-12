import socket
import threading
import argparse
import os
import mimetypes

class HTTPServer():
    headers = {
        'Server': 'CrudeServer',
        'Content-Type': 'text/html',
    }

    status_codes = {
        200: 'OK',
        204: 'No Content',
        404: 'Not Found',
        501: 'Not Implemented',
    }

    def response_line(self, status_code):
        reason = self.status_codes[status_code]
        line = "HTTP/1.1 %s %s\r\n" % (status_code, reason)

        return line.encode()  # call encode to convert str to bytes

    def response_headers(self, extra_headers=None):
        headers_copy = {'Server': 'CrudeServer', 'Content-Type': 'text/html'}

        if extra_headers:
            headers_copy.update(extra_headers)

        headers = ""

        for h in headers_copy:
            headers += "%s: %s\r\n" % (h, headers_copy[h])

        return headers.encode()  # call encode to convert str to bytes

    def handle_request(self, data):

        response_line = self.response_line(status_code=200)

        response_headers = self.response_headers()

        blank_line = b"\r\n"

        response_body = b"""
            <html>
                <body>
                    <h1>Request received!</h1>
                </body>
            </html>
        """

        return b"".join([response_line, response_headers, blank_line, response_body])

    def handle_client(self, conn, addr):
        print('New client from', addr)
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                response = self.handle_request(data)
                conn.sendall(response)
        finally:
            conn.close()

    def handle_request(self, data):
        request = HTTPRequest(data)

        try:
            handler = getattr(self, 'handle_%s' % request.method)
        except AttributeError:
            handler = self.HTTP_501_handler

        response = handler(request)
        return response

    def HTTP_501_handler(self, request):
        response_line = self.response_line(status_code=501)
        response_headers = self.response_headers()
        blank_line = b"\r\n"
        response_body = b"<h1>501 Not Implemented</h1>"
        return b"".join([response_line, response_headers, blank_line, response_body])

    def handle_GET(self, request):
        filename = request.uri.strip('/')  # remove the slash from the request URI

        if not filename:
            path = '../../Desktop/STUDY/WINTER 2022/comp445/python/demo.html'

        if os.path.exists(filename):
            response_line = self.response_line(status_code=200)

            # find out a file's MIME type
            # if nothing is found, just send `text/html`
            content_type = mimetypes.guess_type(filename)[0] or 'text/html'

            extra_headers = {'Content-Type': content_type}
            response_headers = self.response_headers(extra_headers)

            with open(filename, 'rb') as f:
                response_body = f.read()
        else:
            response_line = self.response_line(status_code=404)
            response_headers = self.response_headers()
            response_body = b"<h1>404 Not Found</h1>"

        blank_line = b"\r\n"
        return b"".join([response_line, response_headers, blank_line, response_body])

    def handle_POST(self, request):
        data = request.uri.strip('/')  # remove the slash from the request URI

        if not data:
            response_line = self.response_line(status_code=204) #no content response
        else:
            response_line = self.response_line(status_code=200)

        #does not post anything

        extra_headers = {'Content-Length': len(data)}
        response_headers = self.response_headers(extra_headers)

        blank_line = b"\r\n"
        return b"".join([response_line, response_headers, blank_line, data])

    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    def start(self):
        try:
            listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind((self.host, self.port))
            listener.listen(5)
            print('Echo server is listening at', self.port)
            while True:
                conn, addr = listener.accept()
                self.handle_client(conn, addr)
        finally:
            listener.close()

class HTTPRequest:
    def __init__(self, data):
        self.method = None
        self.uri = None
        self.http_version = "1.1" # default to HTTP/1.1 if request doesn't provide a version

        self.parse(data)

    def parse(self, data):
        lines = data.split(b"\r\n")

        request_line = lines[0]

        words = request_line.split(b" ")

        self.method = words[0].decode()

        if len(words) > 1:
            # sometimes browsers don't send uri for homepage
            self.uri = words[1].decode() # convert bytes to str

        if len(words) > 2:
            self.http_version = words[2]

if __name__ == '__main__':
    server = HTTPServer()
    server.start()