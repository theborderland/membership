#!/usr/bin/env python3

def get_pretix(args):
    from borderland_tool.pretix import PretixAPI
    return PretixAPI(org=args.org,
                     host=args.server,
                     event=args.event,
                     token=args.token,
                     no_ssl=args.no_ssl)
