FROM pretix/standalone:4.7.1

USER root

ENV DJANGO_SETTINGS_MODULE=

RUN pip3 install pretix-passbook pretix-pages pretix-fontpack-free

ARG tag

ENV PYTHONPATH=$PYTHONPATH:/pretix/src

ENV DJANGO_SETTINGS_MODULE=production_settings

RUN pip3 install "git+https://github.com/theborderland/membership.git#subdirectory=pretix-borderland&egg=pretix_borderland&fixme_hash=$TAG" 

RUN cp -r /usr/local/lib/python*/site-packages/pretix_borderland /pretix/src/pretix/plugins/

RUN cp -r /usr/local/lib/python*/site-packages/pretix_borderland/pretix-locale/* /pretix/src/pretix/locale/

RUN chown -R pretixuser /pretix/src/pretix/locale /pretix/src/pretix/plugins/pretix_borderland

USER pretixuser

RUN cd /pretix/src && python3 manage.py makemigrations && make production
