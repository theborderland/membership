#!/bin/bash

PRETIX_ENV=build/pretix/src

if [ ! -e $PRETIX_ENV ]; then
	echo "Run prepare_base_pretix_devenv.sh or `make build` first"
	exit 0
fi

(
	cd $PRETIX_ENV
	pipenv run python manage.py $@
)
