#! /bin/bash

# Show usage
echo "EXECUTE: python httpc.py --help"
python httpc.py --help

# GET methods
echo ""
echo "EXECUTE: python httpc.py get http://httpbin.org/status/418"
python httpc.py get http://httpbin.org/status/418

echo ""
echo "EXECUTE: python httpc.py get -v 'http://httpbin.org/get?course=networking&assignment=1'"
python httpc.py get -v 'http://httpbin.org/get?course=networking&assignment=1'

echo ""
echo "EXECUTE: python httpc.py get -v 'http://httpbin.org/get?course=networking&assignment=1' -o get_output.txt"
python httpc.py get -v 'http://httpbin.org/get?course=networking&assignment=1' -o get_output.txt
echo "EXECUTE cat get_output.txt"
cat get_output.txt

echo ""
echo "EXECUTE: python httpc.py get -v -f hello.txt 'http://httpbin.org/get?course=networking&assignment=1'"
python httpc.py get -v -f hello.txt 'http://httpbin.org/get?course=networking&assignment=1'


# POST methods
echo ""
echo "EXECUTE python httpc.py post -h Content-Type:application/json --d \"{\"Assignment\": 1}\" http://httpbin.org/post"
python httpc.py post -h Content-Type:application/json --d "{\"Assignment\": 1}" http://httpbin.org/post

echo ""
echo "EXECUTE python httpc.py post -h Content-Type:application/json --f file_input.txt http://httpbin.org/post"
python httpc.py post -h Content-Type:application/json --f file_input.txt http://httpbin.org/post

echo ""
echo "EXECUTE python httpc.py post -h Content-Type:application/x-www-form-urlencoded -d blurb=sheeesh http://httpbin.org/post"
python httpc.py post -h Content-Type:application/x-www-form-urlencoded -d blurb=sheeesh http://httpbin.org/post

echo ""
echo "EXECUTE python httpc.py post -h Content-Type:application/json --f 'file_input.txt' http://httpbin.org/post -o post_output.txt"
python httpc.py post -h Content-Type:application/json --f file_input.txt http://httpbin.org/post -o post_output.txt
echo "EXECUTE cat post_output.txt"
cat post_output.txt

echo ""
read -p "Press any key to continue... " -n1 -s

