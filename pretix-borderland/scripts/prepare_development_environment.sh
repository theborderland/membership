#!/bin/bash
PRETIX_TAG=v4.7.1

echo Building local development environment based on Pretix $PRETIX_TAG

mkdir -p build 
git clone --branch v4.7.1 --single-branch --depth 1 https://github.com/pretix/pretix.git build/pretix

pushd build/pretix/src
pipenv --python 3.9 run pip3 install -e . 
