#!/usr/bin/env python3

import argparse

class LotteryCmd:
    def fetch(self, args):
        lottery = self.get_lottery(args)
        lottery.registrations_to_csv()

    def raffle(self, args):
        lottery = self.get_lottery(args)
        lottery.lottery(args.num)

    def losers(self, args):
        lottery = self.get_lottery(args)
        lottery.losers()

    # def control(self, args)

    def get_lottery(self, args):
        from borderland_tool.lottery import Lottery
        return Lottery(get_pretix(args), args.file, args.quota)

    def add_parser(self, subparsers):
        lottery_parser = subparsers.add_parser('lottery', help='Membership Lottery')
        lottery_parser.add_argument("-f", "--file", default="lottery.csv",
                                    help="CSV file to store/load registrations")

        lottery_subparsers = lottery_parser.add_subparsers(dest='lottery_action')
        lottery_subparsers.required = True
        lottery_fetch = lottery_subparsers.add_parser("fetch",
                                                    help="Retrieve registrations from Pretix")
        lottery_fetch.set_defaults(func=self.fetch)
        lottery_raffle = lottery_subparsers.add_parser("raffle",
                                                       help="Draw winners and invite them")
        lottery_raffle.set_defaults(func=self.raffle)
        lottery_raffle.add_argument("-n", "--num", default=1, type=int,
                                    help="Number of winners to draw")
        lottery_parser.add_argument("-q",
                                    "--quota",
                                    type=int,
                                    default=1,
                                    required=True,
                                    help="internal identifier of quota group to invite to (e.g. 1)")
        lottery_losers = lottery_subparsers.add_parser("losers", help="Make a list of losers")
        lottery_losers.set_defaults(func=self.losers)

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
        parser = subparsers.add_parser('fcfs', help='First Come First Served Sale')
        parser.add_argument("-f", "--file", default="registered_without_membership.csv",
                                    help="CSV file to store/load registrations")

        subparsers = parser.add_subparsers(dest='fcfs_action')
        subparsers.required = True

        fetch = subparsers.add_parser("fetch", help="Retrieve registrations without memberships from Pretix")
        fetch.set_defaults(func=self.fetch)

        send_vouchers = subparsers.add_parser("send", help="Send vouchers to all registered users without membership")
        send_vouchers.set_defaults(func=self.send_vouchers)
        parser.add_argument("-q",
                            "--quota",
                            type=int,
                            default=1,
                            required=True,
                            help="internal identifier of quota group to invite to (e.g. 1)")

def replicate(args):
    from borderland_tool.replication import VoucherReplicator
    pretix = get_pretix(args)
    tags = sum(args.tags, []) # flatten
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
                print(",".join([ str(j) for j in i.values() ]))
    elif vars(args)["graphviz"]:
        print(vr.vizualise())
    else:
        vr.replicate(args.force)


def smep(args):
    from borderland_tool.smep import TransferTool
    pretix = get_pretix(args)
    smep = TransferTool(pretix)
    smep.update()
    smep.display()


def unblock_vouchers(args):
    from borderland_tool.voucher import Voucher
    pretix = get_pretix(args)
    vouchers = sum(args.vouchers, [])
    voucher = Voucher(pretix)
    if len(vouchers) > 0:
        voucher.unblock(vouchers)
    else:
        voucher.unblock_all()

def waitlist(args):
    pass


def get_pretix(args):
    from borderland_tool.pretix import PretixAPI
    return PretixAPI(org = args.org,
                     host = args.server,
                     event = args.event,
                     token = args.token,
                     no_ssl = args.no_ssl)

def main():
    parser = argparse.ArgumentParser(description='A collection of things we do with Pretix')
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


    voucher_parser = subparsers.add_parser('unblock_vouchers', help="Unblock vouchers")
    voucher_parser.set_defaults(func=unblock_vouchers)
    voucher_parser.add_argument('vouchers', action='append', metavar='V', nargs='*', default=[])

#    waitlist_parser = subparsers.add_parser('waitlist')
#    waitlist_parser.set_defaults(func=waitlist)
#    waitlist_parser.add_argument('')


    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()

