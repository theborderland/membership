#!/usr/bin/env python3

import get_pretix


class FCFSCmd:
    def get_fcfs(self, args):
        from borderland_tool.fcfs import FCFS
        return FCFS(get_pretix(args), args.file, args.quota)

    def fetch(self, args):
        fcfs = self.get_fcfs(args)
        fcfs.registrations_to_csv()

    def send_vouchers(self, args):
        fcfs = self.get_fcfs(args)
        fcfs.send_vouchers()

    def add_parser(self, subparsers):
        parser = subparsers.add_parser(
            'fcfs', help='First Come First Served Sale')
        parser.add_argument("-f", "--file", default="registered_without_membership.csv",
                            help="CSV file to store/load registrations")

        subparsers = parser.add_subparsers(dest='fcfs_action')
        subparsers.required = True

        fetch = subparsers.add_parser(
            "fetch", help="Retrieve registrations without memberships from Pretix")
        fetch.set_defaults(func=self.fetch)

        send_vouchers = subparsers.add_parser(
            "send", help="Send vouchers to all registered users without membership")
        send_vouchers.set_defaults(func=self.send_vouchers)
        parser.add_argument("-q",
                            "--quota",
                            type=int,
                            default=1,
                            required=True,
                            help="internal identifier of quota group to invite to (e.g. 1)")
