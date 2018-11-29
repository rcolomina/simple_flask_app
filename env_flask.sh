#!/bin/bash

# TODO: Setup environment folder to run source command 
env="testing"

source $env/bin/activate
export FLASK_ENV=development
export FLASK_APP=Flask.py

flask run
