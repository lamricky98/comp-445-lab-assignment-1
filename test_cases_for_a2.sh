#! /bin/bash

# Show usage
echo "EXECUTE: python httpfs.py --help"
python httpfs.py --help

# GET methods
echo ""
echo "EXECUTE: python httpc.py get -v http://localhost:8080/"
python httpc.py get -v http://localhost:8080/

echo ""
echo "EXECUTE: python httpc.py get -v http://localhost:8080/txt-file.txt"
python httpc.py get -v http://localhost:8080/txt-file.txt

echo ""
echo "EXECUTE: python httpc.py get -v http://localhost:8080/subdirectory/foo.txt"
python httpc.py get -v http://localhost:8080/subdirectory/foo.txt

# POST methods
echo ""
echo "EXECUTE: python httpc.py post --d foobar-file-data -v http://localhost:8080/subdirectory/foobar.txt"
python httpc.py post -d foobar-file-data -v http://localhost:8080/subdirectory/foobar.txt

echo ""
echo "EXECUTE: python httpc.py post --f file_input.txt -v http://localhost:8080/data_from_file_input.txt"
python httpc.py post --f file_input.txt -v http://localhost:8080/data_from_file_input.txt

echo ""
echo "EXECUTE: python httpc.py post --d bar-file-data-overwrite -v http://localhost:8080/subdirectory/bar.txt"
python httpc.py post --d bar-file-data-overwrite -v http://localhost:8080/subdirectory/bar.txt

echo ""
read -p "Press any key to continue... " -n1 -s

