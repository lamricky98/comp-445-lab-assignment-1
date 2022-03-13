import socket
import re
import sys

URL_REGEX = "((http[s]?|ftp):\/)?\/?((www\.)?([^:\/\s\?]+))(:(\d+))?(((\/[\w\/]*)?(\.\w+))?(\?([\w=&]+))?)"
blank_line = '\r\n'
content_type = "Content-Type: {content_type}"
content_length = "Content-Length: {content_length}"


"""
Appends a proper header to the GET or POST request.
"""
def build_request(h, d, f, getpost, host, path):
    headersJson = {
        "Host": "",
    }

    if h is not None:
        for header in h:
            split_header = header.split(':')
            header_key = str(split_header[0])
            if ((str(header_key) == "Host" or str(header_key).upper() == "Content-Length".upper())):
                print("The following header could not be overridden: " + header_key + "\n")
            else:
                headersJson[header_key] = split_header[1]

    request = ''.join([getpost, ' ', path, ' HTTP/1.1', blank_line])

    headersJson["Host"] = host

    if headersJson:
        for key, value in headersJson.items():
            headersJson[key] = value
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
                           content_length.format(content_length=len(data_bytes)), blank_line, blank_line,
                           parameters])

    request = ''.join([request, blank_line])
    return request


"""
Performs the GET or POST operation as specified in the getpost parameter.
"""
def process_request(v, h, d, f, getpost, host, port, path, request):
    try:
        socketer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM for TCP
        socketer.connect((host, port))
        socketer.send(request.encode())
        response = ""

        #while True:
            #try:
                #socketer.settimeout(0.2)
                #response += socketer.recv(1024).decode("utf-8")
            #except:
                #break

        response = socketer.recv(4096, socket.MSG_WAITALL).decode("utf-8")

    except:
        print("An error occurred, please retry: ", sys.exc_info())
        sys.exit(0)

    response_arr = response.split(blank_line + blank_line)
    response_headers = response_arr[0]
    response_headers_arr = response_headers.split(blank_line)

    try:
        response_status = int(response_headers_arr[0].split(' ')[1])
    except (IndexError):
        response_status = 200

    #code block for redirection
    if response_status >= 300 and response_status < 400:
        pattern = re.search('(Location: )(.+)', response)
        if (pattern.group(2)):
            newUrl = pattern.group(2)
        else:
            newUrl = "http://httpbin.org/get"
        matcher = re.search(URL_REGEX, newUrl)
        host = matcher.group(5)
        porter = int(matcher.group(7))
        if porter is None:
            porter = port

        pather = matcher.group(8)
        if pather is None:
            pather = path
        print(response_headers_arr[0])

        while True:
            print("Redirect url: ", newUrl)
            answer = input("Do you accept to follow the redirection link? [y/n]: ")
            if answer == 'Y' or answer == 'y':
                requester = build_request(h, d, f, getpost, host, path)
                final_output = process_request(v, h, d, f, getpost, host, port, path, requester)
                break
            elif answer != 'n':
                print("Please enter a valid answer.")
            elif answer == 'n':
                break

    else:
        if v: #verbose output
            final_output = request
            final_output = final_output + response
        else:
            final_output = response_arr[1]

    return final_output
