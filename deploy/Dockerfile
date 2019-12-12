FROM pretix/standalone:stable
USER root
RUN pip3 install pretix-passbook pretix-pages pretix-fontpack-free
ARG tag
RUN pip3 install "git+git://github.com/theborderland/membership.git#subdirectory=pretix-borderland&egg=pretix_borderland&fixme_hash=$TAG" 
RUN cp -r /usr/local/lib/python*/site-packages/pretix_borderland/pretix-locale/en_bl /pretix/src/pretix/locale/
RUN chown -R pretixuser /pretix/src/pretix/locale/en_bl
USER pretixuser
RUN cd /pretix/src && make production
