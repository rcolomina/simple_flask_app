#!/bin/bash
usage()
{
    echo -n "Usage:  $0 <username> <email> <firstname> <surname>"
    echo " "
    exit 1
}

[[ $# -ne 4 ]] && usage

username=$1
email=$2
first=$3
surname=$4

mydata="{\"username\":\"${username}\",\"email\":\"${email}\",\"firstname\":\"${first}\",\"surname\":\"${surname}\"}"

echo "POST data for curl: "$mydata
curl --header "Content-type: application/json" --request POST --data $mydata 127.0.0.1:5000/contact/

