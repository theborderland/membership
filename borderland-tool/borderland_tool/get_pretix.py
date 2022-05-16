#!/usr/bin/env python3
from borderland_tool.pretix import PretixAPI


def get_pretix(args):
    return PretixAPI(org=args.org,
                     host=args.server,
                     event=args.event,
                     token=args.token,
                     no_ssl=args.no_ssl)