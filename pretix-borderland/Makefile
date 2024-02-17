VENV=$(shell pipenv --venv)
Command := $(firstword $(MAKECMDGOALS))
Arguments := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))

.PHONY: all 
all: build

.PHONY: build 
build: $(VENV)
	@pipenv run python setup.py develop
	@echo "\n\n\n*******************************************************************************\n"
	@echo "Membertix build finished."
	@echo "To run Membertix in dev mode run:"
	@echo "\tsh pipenv run python -m pretix runserver\n"

$(VENV): 
	@sh scripts/prepare_base_pretix_devenv.sh

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
	@pipenv -rm

%::
	@true
