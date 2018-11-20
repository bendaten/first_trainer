#!/usr/bin/env bash

export FIRST_TRAINER=~/PycharmProjects/first_trainer/
echo "$@"
python3 ${FIRST_TRAINER}/src/main.py "$@"