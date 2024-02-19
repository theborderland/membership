FROM pretix/standalone:4.7.1

USER root

ENV DJANGO_SETTINGS_MODULE=

RUN pip3 install "pretix-passbook==1.9.1" "pretix-pages==1.4.1" "pretix-fontpack-free==1.8.0"

ARG tag

ENV PYTHONPATH=$PYTHONPATH:/pretix/src

ENV DJANGO_SETTINGS_MODULE=production_settings

RUN pip3 install "git+https://github.com/theborderland/membership.git#subdirectory=pretix-borderland&egg=pretix_borderland&fixme_hash=$TAG" 

RUN pip3 install "django-mysql==4.5.0" django_countries

RUN cp -r /usr/local/lib/python*/site-packages/pretix_borderland /pretix/src/pretix/plugins/ && \
	cp -r /usr/local/lib/python*/site-packages/pretix_borderland/pretix-locale/* /pretix/src/pretix/locale/ && \
	chown -R pretixuser /pretix/src/pretix/locale /pretix/src/pretix/plugins/pretix_borderland

WORKDIR /pretix/src

RUN python3 manage.py makemigrations 
RUN make production

USER pretixuser
