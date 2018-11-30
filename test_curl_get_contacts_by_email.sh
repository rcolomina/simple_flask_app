#!/bin/bash
usage()
{
    echo -n "Usage:  $0 <email>"
    echo " "
    exit 1
}

[[ $# -ne 1 ]] && usage

email=$1
IP="127.0.0.1"
PORT="5000"
route="/contact/email/${email}"
URI="${IP}:${PORT}${route}"
header="Content-type: application/json"
command="GET"
data=""

echo "curl command was send with parameters:"
echo "header   "$header
echo "request  "$command
echo "data     "$data
echo "URI      "$URI

echo "curl --header \"$header\" --request $command $data $URI"
curl --header "$header" --request $command $URI


