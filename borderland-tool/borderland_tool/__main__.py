#!/usr/bin/env python3

import argparse

import replicate
import smep
import unblock_vouchers
import LotteryCmd
import FCFSCmd


def waitlist(args):
    pass


def main():
    parser = argparse.ArgumentParser(
        description='A collection of things we do with Pretix')
    subparsers = parser.add_subparsers(dest='cmd')
    subparsers.required = True

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
                        default="2022", help="pretix event to operate on")
    parser.add_argument("-N", "--no-ssl", action='store_true',
                        help="disable ssl when communicating with pretix, good for testing locally")

    # Transfers
    smep_parser = subparsers.add_parser('smep', help='Membership Transfers')
    smep_parser.set_defaults(func=smep)

    # Lottery
    lotterycmd = LotteryCmd()
    lotterycmd.add_parser(subparsers)

    # Firs Come, First Served Sale (FCFS)
    fcfs = FCFSCmd()
    fcfs.add_parser(subparsers)

    # Replicating Vouchers
    replicate_parser = subparsers.add_parser('replicate',
                                             help="replicating +1 vouchers")
    replicate_parser.set_defaults(func=replicate)

    replicate_parser.add_argument("-p", "--print",
                                  action='store_true',
                                  help="print list of pending invites")
    replicate_parser.add_argument("-g", "--graphviz",
                                  action='store_true',
                                  help="make a DOT graph")
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

    voucher_parser = subparsers.add_parser(
        'unblock_vouchers', help="Unblock vouchers")
    voucher_parser.set_defaults(func=unblock_vouchers)
    voucher_parser.add_argument(
        'vouchers', action='append', metavar='V', nargs='*', default=[])

#    waitlist_parser = subparsers.add_parser('waitlist')
#    waitlist_parser.set_defaults(func=waitlist)
#    waitlist_parser.add_argument('')

    args = parser.parse_args()
    print("args={}".format(args))
    args.func(args)


if __name__ == "__main__":
    main()
