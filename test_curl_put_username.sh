#!/bin/bash
usage()
{
    echo -n "Usage:  $0 <email> <email> <firstname> <surname>"
    echo " "
    echo "This updates a contact setting: username,email,firstname and surname"
    echo " "
    exit 1
}

[[ $# -ne 4 ]] && usage

username=$1
email=$2
firstname=$3
surname=$4
mydata="{\"email\":\"${email}\",\"firstname\":\"${firstname}\",\"surname\":\"${surname}\"}"

echo "PUT data for curl: "$mydata
curl --header "Content-type: application/json" --request PUT --data $mydata 127.0.0.1:5000/contact/$username

