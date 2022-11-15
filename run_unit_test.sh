#!/bin/bash

pip install -r requirements.txt
PYTHONPATH=$(pwd)/src/ticker pytest --cov-report html --cov src/ticker --cov-fail-under=90