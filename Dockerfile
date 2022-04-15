FROM pretix/standalone:4.7.1

USER root

RUN pip3 install pretix-passbook pretix-pages pretix-fontpack-free

ARG tag

RUN pip3 install "git+https://github.com/theborderland/membership.git#subdirectory=pretix-borderland&egg=pretix_borderland&fixme_hash=$TAG" 

RUN cp -r /usr/local/lib/python*/site-packages/pretix_borderland/pretix-locale/* /pretix/src/pretix/locale/

RUN chown -R pretixuser /pretix/src/pretix/locale/

USER pretixuser

RUN cd /pretix/src && make all
