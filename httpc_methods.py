import socket
import re
import sys

URL_REGEX = "((http[s]?|ftp):\/)?\/?((www\.)?([^:\/\s\?]+))(:(\d+))?(((\/[\w\/]*)?(\.\w+))?(\?([\w=&]+))?)"
blank_line = '\r\n'
path = "/"
port = 80
contentType = "Content-Type: {content_type}"
contentLength = "Content-length: {content_length}"


def is_valid_header(key):
    if (str(key) == "Host" or str(key) == "Content-length"):
        return False
    return True


# #######################
# Build HTTP request
# #######################

def build_request(v, h, d, f, getpost, host, port, path):
    headersJson = {
        "Host": "",
        "Connection": "Keep-Alive"
    }

    if h is not None:
        for header in h:
            split_header = header.split(':')
            header_key = str(split_header[0])
            if (not (is_valid_header(header_key))):
                print("Cannot override header: " + header_key + "\n")
            else:
                headersJson[header_key] = split_header[1]

    request = ''.join([getpost, ' ', path, ' HTTP/1.1', blank_line])

    headersJson["Host"] = host

    if headersJson:
        for key, value in headersJson.items():
            headersJson[key] = value
            request = ''.join([request, key, ':', value, blank_line])

    if headersJson:
        for key, value in headersJson.items():
            request = ''.join([request, key, ': ', value, blank_line])

    if getpost == "POST":
        parameters = ''
        if f is None:
            parameters = d
        else:
            f = open(f, 'r')
            for line in f:
                if line:
                    parameters += line.rstrip('\n') + '&'

        if parameters[-1] == '&':
            parameters = parameters.rstrip('&')

        data_bytes = parameters.encode()
        request = ''.join([request,
                           contentLength.format(content_length=len(data_bytes)), blank_line, blank_line,
                           parameters])

    request = ''.join([request, blank_line])
    return request


# #######################
# Process Http Request
# #######################
def process_request(v, h, d, f, getpost, host, port, path, request):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM for TCP
        s.connect((host, port))
        s.send(request.encode())
        responseBytes = s.recv(4096)
        response = responseBytes.decode()
    except:
        print("An error occurred, please retry: ", sys.exc_info())
        sys.exit(0)

    response_arr = response.split(blank_line + blank_line)
    response_headers = response_arr[0]
    response_headers_arr = response_headers.split(blank_line)
    response_status = parse_response_status(response_headers)

    if response_status >= 300 and response_status < 400:

        newUrl = parse_redirect_url_for_300(response)
        matcher = re.search(URL_REGEX, newUrl)
        host = matcher.group(5)
        port = int(matcher.group(7))
        if port is None:
            port = port

        pather = matcher.group(8)
        if pather is None:
            pather = path
        print(response_headers_arr[0])
        print("Redirect url: ", newUrl)
        answer = input("Do you accept to follow the redirection link? [Y/n]: ")
        if answer != 'n':
            requester = build_request(v, h, d, f, getpost, host, port, path)
            final_output = process_request(v, h, d, f, getpost, host, port, path, requester)

    else:
        if v:
            final_output = response
        else:
            final_output = response_arr[1]

    return final_output


# #######################
# Extract response status
# #######################
def parse_response_status(response_headers):
    response_headers_arr = response_headers.split(blank_line)
    response_status = int(response_headers_arr[0].split(' ')[1])
    return response_status


# #######################
# Extract redirect url
# #######################
def parse_redirect_url_for_300(response):
    pattern = re.search('(Location: )(.+)', response)
    return pattern.group(2)
    return "http://httpbin.org/get"
