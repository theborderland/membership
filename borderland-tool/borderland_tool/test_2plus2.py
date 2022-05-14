from threading import local
import unittest
from borderland_tool.lotterycmd import LotteryCmd
from borderland_tool.get_pretix import get_pretix
import argparse


class Test2Plus2(unittest.TestCase):
    lotterycmd = LotteryCmd()

    def setUp(self):
        pass

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

    # def test_get_pretix_not_null(self):
    #     args = self.theparser.parse_args()
    #     print("after args")
    #     pretix = get_pretix(args)
    #     self.assertIsNotNone(pretix)

    def tearDown(self):
        pass
