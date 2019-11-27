#!/usr/bin/env python3

import argparse

def replicate(args):
    from replication import VoucherReplicator
    pretix = get_pretix(args)
    tags = sum(args.tags, []) # flatten
    if args.all_vouchers:
        tags = None
    vr = VoucherReplicator(pretix,
                           tags,
                           args.quota,
                           args.pref_name_id,
                           args.invite_id)
    if vars(args)["print"]:
        invites = vr.invites_to_send()
        if invites:
            print(",".join(invites[0].keys()))
            for i in invites:
                print(",".join([ str(j) for j in i.values() ]))
    else:
        vr.replicate(args.force)


def get_pretix(args):
    from pretix import PretixAPI
    return PretixAPI(org = args.org,
                     host = args.server,
                     event = args.event,
                     token = args.token)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A collection of things we do with Pretix')
    subparsers = parser.add_subparsers()

    # Common Arguments
    parser.add_argument("-t", "--token",
                        required=True,
                        help="api token for pretix (required)")
    parser.add_argument("-s", "--server", metavar="HOST",
                        default="localhost:8000",
                        help="hostname of pretix instance")
    parser.add_argument("-o", "--org",
                        default="test",
                        help="pretix organisation to operate on")
    parser.add_argument("-e", "--event",
                        default="2020", help="pretix event to operate on")

    # Replicating Vouchers
    replicate_parser = subparsers.add_parser('replicate',
                                             help="replicating +1 vouchers")
    replicate_parser.set_defaults(func=replicate)

    replicate_parser.add_argument("-p", "--print",
                                  action='store_true',
                                  help="print list of pending invites")
    replicate_parser.add_argument("-f", "--force",
                                  action='store_true',
                                  help="don't ask for confirmation")
    replicate_parser.add_argument("-a", "--all-vouchers",
                                  action='store_true',
                                  help="replicate all voucher tags")
    replicate_parser.add_argument("-q",
                                  "--quota",
                                  type=int,
                                  required=True,
                                  help="internal identifier of quota group to invite to (e.g. 1)")
    replicate_parser.add_argument("-t", "--tags",
                                  action='append',
                                  metavar="TAG",
                                  nargs="+",
                                  default=[],
                                  help="only replicate orders made with these voucher tags (\"lottery\", \"board\", ...)")
    replicate_parser.add_argument("--pref-name-id",
                                  default="prefname",
                                  help="question identifier for user's preferred name")
    replicate_parser.add_argument("--invite-id",
                                  default="invite",
                                  help="question identifier for e-mail address to be invited")


    args = parser.parse_args()
    args.func(args)
