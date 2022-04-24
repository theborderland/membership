# Borderland Membership tools

This is the stuff we use for selling memberships for the Borderland. The long
term goal for this is to distill it into a couple of Pretix plugins that does
what we want. To do that we first need to know what we want, so things are a bit
experimental at the moment.

We use a combination of lottery and replicating invitations to distribute
memberships, trying to find a good alternative to first come first served sales.

Overview:

- `borderland-tool/` - A command line tool (blt) that uses the Pretix API to do most of the long-running and one-off tasks
- `docs/` - Collection of writings and checklists
- `membership-card/` - Components for the ticket design
- `pretix-borderland/` - Our Pretix plugin with experiments in it

Instructions for running membertix locally are located in `docs/running_locally.md`
