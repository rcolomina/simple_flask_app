#!/bin/bash
usage()
{
    echo -n "Usage:  $0 <username>"
    echo " "
    exit 1
}

[[ $# -ne 1 ]] && usage

username=$1
IP="127.0.0.1"
PORT="5000"
route=/contact/$username
URI="$IP:$PORT$route"
header="Content-type: application/json"
command="DELETE"

echo "curl command was send with parameters:"
echo "header   "$header
echo "request  "$command
echo "URI      "$URI
echo "curl --header \"$header\" --request $command $URI"
curl --header "$header" --request $command $URI


