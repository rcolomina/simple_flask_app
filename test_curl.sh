#!/bin/bash

username=$1
mydata="{\"username\":\"${username}\"}"
echo "Data to send using curl:"$mydata
curl --header "Content-type: application/json" --request POST --data $mydata 127.0.0.1:5000/contact/

