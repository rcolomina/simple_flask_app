#!/bin/bash

source testing/bin/activate
export FLASK_ENV=development
export FLASK_APP=Flask.py

flask run
