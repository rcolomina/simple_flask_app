#!/bin/bash

username=""
IP="127.0.0.1"
PORT="5000"
route="/contact/$username"
URI="$IP:$PORT$route"
header="Content-type: application/json"
command="GET"

echo "curl --header \"$header\" --request $command $URI"
curl --header "$header" --request $command $URI



