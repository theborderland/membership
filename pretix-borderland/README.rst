Pretix Borderland Plugin
========================

This is a django plugin for `pretix`, that provides locales, email templates,
new pages, and functionality that is specific to the Borderland but that can be
easily reused by other events.



Development setup
-----------------
Make sure you have installed GNU `make` as well as `python` 3.11.2 and `pipenv`.

0. Make sure you have installed in your system the following tools.

   * GNU Make (`make`)
   * Python 3.11
   * Pipenv (`pipenv`)
   * NPM (`npm`).

   Notes:
   If you run from Windows I recommend to use WSL directly and run this on
   debian or ubuntu. Other solutions (using chocolatey + brew may work but I
   haven't succeed).
   On Mac, make sure to install `brew` and brew gnu `make` with it and make
   sure the system points to the gnu make instead of the local one.

1. From this directory run `make`

   The first time you setup your environment this way, `make` will create a
   virtual environment where it will install pretix with all its dependencies.
   The script at this stage will also execute django-admin makemigrations and
   migrate. Note that runing `pretix` in this mode will use sqlite (and not
   postgres) as in production, which simplifies things for development.
   
   The environment setup will take 6-10 minutes, but it's done only once, until
   you decide to clear it out (you can do so by removing the
   `pretix-borderland/build` directory.

   All subsequent times you invoke `make` or `make build` to rebuild the plugin. 

2. Now spin up Membertix (`pretix` + this plugin) in local:

   pipenv run python -m pretix runserver

3. Do the changes you need to do to the plugin and execute `make` while the
   server is running. Django will detect the changes and auto-reload them so 
   you can see them in your local browser without stopping the server.


License
-------

Copyright 2019 Kris, Michi et al
Copyright 2022 The Borderland Tech Team
Copyright 2023 @darkturo

Released under the terms of the Apache License 2.0


References
----------
.. _pretix: https://github.com/pretix/pretix
.. _pretix development setup: https://docs.pretix.eu/en/latest/development/setup.html
