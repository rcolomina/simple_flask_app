#!/bin/bash
username=$1
echo "username:"$username
curl --header "Content-type: application/json" --request DELETE 127.0.0.1:5000/contact/$username

