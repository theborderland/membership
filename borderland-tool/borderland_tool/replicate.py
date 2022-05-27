#!/usr/bin/env python3

from borderland_tool.get_pretix import get_pretix
from borderland_tool.replication import VoucherReplicator


def replicate(args):
    pretix = get_pretix(args)
    tags = sum(args.tags, [])  # flatten
    if args.all_vouchers:
        tags = None
    vr = VoucherReplicator(pretix,
                           tags,
                           args.quota,
                           args.invite_id,
                           args.pref_name_id)
    if vars(args)["print"]:
        invites = vr.invites_to_send()
        if invites:
            print(",".join(invites[0].keys()))
            for i in invites:
                print(",".join([str(j) for j in i.values()]))
    elif vars(args)["graphviz"]:
        print(vr.vizualise())
    else:
        vr.replicate(args.force)
