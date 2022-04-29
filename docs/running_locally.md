# Running and Testing Membertix and the Borderland-tool locally

A good way to get acquainted with the project, and perhaps the best way
to test quick fixes in your local machine without having to setup a pretix
development environemnt, is to use docker and docker-compose.

## Running Membertix locally

You can run Membertix (Pretix + The Borderland memberships Plugin) locally
using the `docker-comopose` configuration file available in this repository.

To do this build a docker image with your latest changes in the repository.
You can use the available makefile as follows:

```
make
```

Windows: Install Cygwin, reinstall Docker and run `make`. Currently there is an issue running from Powershell or the default commandline.
After the image is built (it may take a few minutes), you can execute pretix
locally and start testing:

```
docker-compose up
```

Once it's running you'll be able to see locally in your broser a barebone
installation of "Membertix" which you can use to test your code changes.

You can do by opening `http://localhost:8000` on your browser

You may be able to register yourself or use the default user `admin@localhost`
and password `admin`.

OBS: this is disblaed in production for obvious reasons

### Emails

By default I have setup docker-compose to use a fake email server, which you
could use to check if emails and content is being sent correctly.

You could check the emails that are being delivered to the mailserver
by curling on the port 1080::

```
curl -v http://localhost:1080/api/emails
```

## Running the borderland-tool locally against a local me

Addionally you should be able to run the borderland tool towards your local setup.

To do so, you can setup a virtual environemnt for the tool (you can choose, but
for the sake of the example I'll use pipenv, which is my favorite).

```
cd borderland-tool
pipenv --python 3.9 install -r requirements.txt
```

Then you could use the help command as usual:

```
borderland-tool $ python borderland_tool -h
usage: borderland_tool [-h] -t TOKEN [-s HOST] [-o ORG] [-e EVENT]
                       {smep,lottery,replicate,unblock_vouchers} ...

A collection of things we do with Pretix

positional arguments:
  {smep,lottery,replicate,unblock_vouchers}
    smep                Membership Transfers
    lottery             Membership Lottery
    replicate           replicating +1 vouchers
    unblock_vouchers    Unblock vouchers

optional arguments:
  -h, --help            show this help message and exit
  -t TOKEN, --token TOKEN
                        api token for pretix (required)
  -s HOST, --server HOST
                        hostname of pretix instance
  -o ORG, --org ORG     pretix organisation to operate on
  -e EVENT, --event EVENT
                        pretix event to operate on

```

### Running the lottery

The lottery runs in two steps:

- Fetch all the registered users

```
python borderland_tool -t localhost:8000/token -s localhost:8000 -o ORGANISATION -e EVENT lottery -q QUOTA -f registrations.csv fetch
```

If there is no local registration CSV file, one will be created from the existing registrations in pretix. Otherwise, an existing CSV file is augmented by new entries since last run.

TODO: specify where the token should come from, and where to find the name of Organization and Event

- Run the lottery and send purchase vouchers to the event to the winners

```
python borderland_tool -t localhost:8000/token -s localhost:8000 -o ORGANISATION -e EVENT raffle -q QUOTA -f registrations.csv
```
