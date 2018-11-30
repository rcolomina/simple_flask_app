#!/bin/bash
username=$1

mydata="{\"username\":\"$username\",\"email\":[\"frodobolson2@mordor.com\",\"fbolson3@earth.com\",\"frodobolson4@mordor.com\"],\"firstname\":\"Frodo\",\"surname\":\"BolsonCerrado\"}"

echo "Data to send using curl: "$mydata
curl --header "Content-type: application/json" --request PUT --data $mydata 127.0.0.1:5000/contact/$username
