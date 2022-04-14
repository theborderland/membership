all: localecompile

localecompile:
	django-admin compilemessages

localegen:
	django-admin makemessages --keep-pot -i build -i dist -i "*egg*" -l en_BL

.PHONY: all localecompile localegen
