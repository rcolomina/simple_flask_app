#!/bin/bash
username=$1
email=$2
firstname=$3
surname=$4

echo "username:"$username
echo "email:"$email
echo "firstname:"$firstname
echo "surname:"$surname

mydata="{\"email\":\"${email}\",\"firstname\":\"${firstname}\",\"surname\":\"${surname}\"}"
echo "Data to send using curl:"$mydata
curl --header "Content-type: application/json" --request PUT --data $mydata 127.0.0.1:5000/contact/$username

