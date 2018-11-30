#!/bin/bash
usage()
{
    echo -n "Usage:  $0 <username>"
    echo " "
    echo "This updates a contact by username."
    echo " "
    exit 1
}

[[ $# -ne 1 ]] && usage

username=$1

mydata="{\"username\":\"$username\",\"email\":[\"frodobolson2@mordor.com\",\"fbolson3@earth.com\",\"frodobolson4@mordor.com\"],\"firstname\":\"Frodo\",\"surname\":\"BolsonCerrado\"}"

echo "PUT data for curl: "$mydata
curl --header "Content-type: application/json" --request PUT --data $mydata 127.0.0.1:5000/contact/$username
