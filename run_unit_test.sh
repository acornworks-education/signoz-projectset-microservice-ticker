#!/bin/bash

pip install -r requirements.txt
pytest --cov-report html --cov src/ticker --cov-fail-under=90