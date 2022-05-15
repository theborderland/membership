import unittest
from borderland_tool.lotterycmd import LotteryCmd
from borderland_tool.get_pretix import get_pretix
import argparse


class TestParsers(unittest.TestCase):
    lotterycmd = LotteryCmd()

    def setUp(self):
        self.parser = argparse.ArgumentParser(
            description='A collection of things we do with Pretix')
        subparsers = self.parser.add_subparsers(dest='cmd')
        subparsers.required = True

        # Common Arguments
        self.parser.add_argument("-t", "--token",
                                 required=True,
                                 help="api token for pretix (required)")
        self.parser.add_argument("-s", "--server", metavar="HOST",
                                 default="localhost:8000",
                                 help="hostname of pretix instance")
        self.parser.add_argument("-o", "--org",
                                 default="test",
                                 help="pretix organisation to operate on")
        self.parser.add_argument("-e", "--event",
                                 default="2022", help="pretix event to operate on")
        self.parser.add_argument("-N", "--no-ssl", action='store_true',
                                 help="disable ssl when communicating with pretix, good for testing locally")

        # Lottery
        lotterycmd = LotteryCmd()
        lotterycmd.add_parser(subparsers)

    def test_argparse(self):
        simple_parser = argparse.ArgumentParser(
            description='Simple parser to test')
        simple_parser.add_argument("-a", "--arg1",
                                   required=True,
                                   help="first argument (required)")
        simple_parser.add_argument("-b", "--arg2",
                                   required=True,
                                   help="second argument (required)")

        cmd_args = ['--arg1', 'asdf', '--arg2', 'qwer']
        result_args = simple_parser.parse_args(cmd_args)
        self.assertEqual(len(cmd_args), 4)
        self.assertEqual(result_args.arg1, "asdf")
        self.assertEqual(result_args.arg2, "qwer")
        short_args = ['-a', 'ASDF', '-b', 'QWER']
        result_args = simple_parser.parse_args(short_args)
        self.assertEqual(result_args.arg1, "ASDF")
        self.assertEqual(result_args.arg2, "QWER")

    def test_lottery_args_fetch(self):
        cmd_args = ['-t', 'mytoken', '-s', 'myserver',
                    '-o', 'myorg', '-e', 'myevent',
                    'lottery', '-q', '88', 'fetch']
        args = self.parser.parse_args(cmd_args)
        self.assertEqual(args.cmd, 'lottery')
        self.assertEqual(args.lottery_action, 'fetch')
        self.assertEqual(args.quota, 88)
        pretix = get_pretix(args)
        self.assertIsNotNone(pretix)
        self.assertEqual(pretix.org, "myorg")
        self.assertEqual(pretix.host, "myserver")
        self.assertEqual(pretix.event, "myevent")
        self.assertEqual(pretix.token, "mytoken")

    def test_lottery_args_raffle(self):
        cmd_args = ['-t', 'mytoken', '-s', 'myserver',
                    '-o', 'myorg', '-e', 'myevent',
                    'lottery', '-q', '88', 'raffle', '-n', '10']
        args = self.parser.parse_args(cmd_args)
        self.assertEqual(args.cmd, 'lottery')
        self.assertEqual(args.lottery_action, 'raffle')
        self.assertEqual(args.quota, 88)
        pretix = get_pretix(args)
        self.assertIsNotNone(pretix)
        self.assertEqual(pretix.org, "myorg")
        self.assertEqual(pretix.host, "myserver")
        self.assertEqual(pretix.event, "myevent")
        self.assertEqual(pretix.token, "mytoken")

    def tearDown(self):
        pass
