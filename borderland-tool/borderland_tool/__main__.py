#!/usr/bin/env python3

import argparse

class LotteryCmd:
    def fetch(self, args):
        lottery = self.get_lottery(args)
        lottery.registrations_to_csv()

    def raffle(self, args):
        lottery = self.get_lottery(args)
        lottery.lottery(args.num)

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
    else:
        vr.replicate(args.force)


def smep(args):
    from borderland_tool.smep import TransferTool
    pretix = get_pretix(args)
    smep = TransferTool(pretix)
    smep.update()
    smep.display()


def get_pretix(args):
    from borderland_tool.pretix import PretixAPI
    return PretixAPI(org = args.org,
                     host = args.server,
                     event = args.event,
                     token = args.token)

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
                        default="2020", help="pretix event to operate on")

    # Transfers
    smep_parser = subparsers.add_parser('smep', help='Membership Transfers')
    smep_parser.set_defaults(func=smep)

    # Lottery
    lotterycmd = LotteryCmd()
    lotterycmd.add_parser(subparsers)

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

if __name__ == "__main__":
    main()

