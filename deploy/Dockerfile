FROM pretix/standalone:stable
USER root
RUN pip3 install pretix-passbook pretix-pages pretix-fontpack-free
ARG tag
RUN pip3 install "git+git://github.com/theborderland/membership.git#subdirectory=pretix-borderland&egg=pretix_borderland&fixme_hash=$TAG" 
USER pretixuser
RUN cd /pretix/src && make production
