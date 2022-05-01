#!/bin/bash
PRETIX_TAG=v4.7.1

echo Building local development environment based on Pretix $PRETIX_TAG

mkdir -p build 
git clone --branch v4.7.1 --single-branch --depth 1 https://github.com/pretix/pretix.git build/pretix

(
	BASE_DIR=$(pwd)
	cd build/pretix/src

	pipenv --rm
	pipenv --python 3.9 install -e .

	ln -s $BASE_DIR/pretix_borderland/pretix-locale/en_BL pretix/locale
	ln -s $BASE_DIR/pretix_borderland pretix/plugins

)
