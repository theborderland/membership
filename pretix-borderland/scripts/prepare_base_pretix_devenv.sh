#!/bin/bash
#PRETIX_TAG=v4.7.1
PRETIX_TAG=v2024.1.0

echo Building local development environment based on Pretix $PRETIX_TAG

mkdir -p build 
git clone --branch $PRETIX_TAG --single-branch --depth 1 https://github.com/pretix/pretix.git build/pretix

(
	BASE_DIR=$(pwd)
	TARGET_DIR=$BASE_DIR/build/pretix/src
	cd $TARGET_DIR


	pipenv --rm
	pipenv --python 3.11.2 install django django-mysql django-filter django-formset-js djangorestframework django-compressor importlib_metadata kombu pycountry 

	ln -s $BASE_DIR/pretix_borderland/pretix-locale/en_BL pretix/locale
	ln -s $BASE_DIR/pretix_borderland pretix/plugins

)
