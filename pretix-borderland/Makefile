PRETIX_TAG=v2024.1.0

Command := $(firstword $(MAKECMDGOALS))
Arguments := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))

VENV=$(shell pipenv --venv 2> /dev/null)
ifeq ($(VENV),)
VENV:= download_pretix
else
VENV:=
endif

.PHONY: all 
all: build

.PHONY: build 
build: $(VENV)
	@pipenv run python setup.py develop
	@echo "\n\n\n*******************************************************************************\n"
	@printf 'Membertix build \e[1;32mfinished\e[0m.\n'
	@echo "To run Membertix in dev mode run:"
	@printf '\t\e[1mpipenv run python -m pretix runserver\e[0m\n\n'

.PHONY: download_pretix
download_pretix:
	@echo Downloading pretix ...
	pipenv --python 3.11.2 run pip3 install -U "git+https://github.com/pretix/pretix.git@$(PRETIX_TAG)#egg=pretix"
	pipenv run python -m pretix migrate
	pipenv run python -m pretix rebuild
	pipenv run python -m pretix updatestyles

.PHONY: run
run: 
	@pipenv run python -m pretix runserver

.PHONY: membertix pretix django
membertix pretix django: 
	@pipenv run python -m pretix "$(Arguments)"


.PHONY: test
test:
	@pipenv run python -m pretix test

.PHONY: clean
clean:
	@pipenv --rm

%::
	@true
