PLUGIN_DIR=$(PWD)
PRETIX_DEVENV=$(PLUGIN_DIR)/build/pretix/src
DJANGO=sh $(PLUGIN_DIR)/scripts/local-django.sh

all: build

env: $(PRETIX_DEVENV) 
build/pretix/src:
	@sh scripts/prepare_base_pretix_devenv.sh
	@cd $(PRETIX_DEVENV); pipenv run python $(PLUGIN_DIR)/setup.py develop
	$(call DJANGO) makemessages -l en_BL
	$(call DJANGO) compilemessages
	$(call DJANGO) collectstatic --noinput
	$(call DJANGO) makemigrations
	$(call DJANGO) migrate

build: env
	@cd $(PRETIX_DEVENV); pipenv run pip3 install $(PLUGIN_DIR)
	@echo "To run Membertix in dev mode run:\n\tsh scripts/local-django.sh runserver\n"

clean:
	rm -rf build

.PHONY: all build env localecompile localegen clean
