#!/bin/sh
usage()
{
    echo -n "Usage:  $0 <username>"
    echo " "
    exit 1
}

[[ $# -ne 1 ]] && usage

username=$1

mydata="{\"username\":\"$username\",\"email\":[\"frodobolson@mordor.com\",\"fbolson@earth.com\"],\"firstname\":\"Frodo\",\"surname\":\"BolsonCerrado\"}"

echo "POST data for curl: "$mydata
curl --header "Content-type: application/json" --request POST --data $mydata 127.0.0.1:5000/contact/

