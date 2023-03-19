#!/bin/bash

PRETIX_DEV_ENV=build/pretix/src

if [ ! -e $PRETIX_DEV_ENV ]; then
	echo "Run prepare_base_pretix_devenv.sh or `make build` first"
	exit 0
fi

(
	cd $PRETIX_DEV_ENV
	PATH=$PATH:$(pipenv --venv)/bin PYTHONPATH=$PATH:$(pipenv --venv)/lib/python3.9/site-packages pipenv run python3 manage.py test $@
)
