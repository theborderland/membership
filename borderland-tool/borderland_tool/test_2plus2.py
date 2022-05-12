import unittest
from LotteryCmd import *
import argparse


class Test2Plus2(unittest.TestCase):
    lotterycmd = LotteryCmd()

    def setUp(self):
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

        self.lotterycmd.add_parser(subparsers)
        print('setUp method called!!')

    def test_string(self):
        a = 'some'
        b = 'some'
        print("lotterycmd="+self.lotterycmd)
        self.assertEqual(a, b)

    def test_2plus2(self):
        a = 2
        b = 2
        self.assertEqual(a + b, 4)

    def tearDown(self):
        print('teardown method called!!')
