#!/bin/bash

username=$1
curl --header "Content-type: application/json" --request GET 127.0.0.1:5000/contact/$username

