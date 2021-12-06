#!/bin/sh
export FLASK_APP=./DEAP/index.py
flask run -h 0.0.0.0 -p 54321
