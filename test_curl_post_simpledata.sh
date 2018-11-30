#!/bin/bash
echo "POST data sing curl: "'Simple string as data'

curl --header "Content-type: application/json" --request POST --data 'Simple string as data' 127.0.0.1:5000/contact



