#!/usr/bin/python3

from borderland_tool.get_pretix import get_pretix
from borderland_tool.lottery import Lottery


class LotteryCmd:
    def fetch(self, args):
        lottery = self.get_lottery(args)
        lottery.registrations_to_csv()
        return lottery

    def raffle(self, args):
        lottery = self.get_lottery(args)
        lottery.lottery(args.num)

    def losers(self, args):
        lottery = self.get_lottery(args)
        lottery.losers()

    # def control(self, args)

    def get_lottery(self, args):
        return Lottery(get_pretix(args), args.file, args.quota)

    def add_parser(self, subparsers):
        lottery_parser = subparsers.add_parser(
            'lottery', help='Membership Lottery')
        lottery_parser.add_argument("-f", "--file", default="lottery.csv",
                                    help="CSV file to store/load registrations")

        lottery_subparsers = lottery_parser.add_subparsers(
            dest='lottery_action')
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
        lottery_losers = lottery_subparsers.add_parser(
            "losers", help="Make a list of losers")
        lottery_losers.set_defaults(func=self.losers)
