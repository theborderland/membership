#!/bin/bash
#PRETIX_TAG=v4.7.1
PRETIX_TAG=v2024.1.0

pipenv --rm
pipenv --python 3.11.2 run pip3 install -U "git+https://github.com/pretix/pretix.git@$PRETIX_TAG#egg=pretix"
pipenv run python -m pretix migrate
pipenv run python -m pretix rebuild
pipenv run python -m pretix updatestyles
