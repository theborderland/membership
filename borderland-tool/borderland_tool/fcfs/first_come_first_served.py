#!/usr/bin/python3
import csv
import random
import json

from datetime import datetime, timezone, timedelta
from dateutil import parser


class FCFS:
    def __init__(self, pretix, csvfile, quota, low_income_quota):
        self.pretix = pretix
        self.csvfile = csvfile
        self.quota = quota
        self.low_income_quota = low_income_quota
        self.registered_without_membership_csv = self.load_csv()
        self.has_order = self.has_voucher = None

    def registrations_to_csv(self):
        self.registered_without_membership_csv = self.pretix.get_registrations_without_membership()
        print("Found {} member(s) registered to the lottery without a membership...".format(len(self.registered_without_membership_csv)))
        self.save_csv()

    def send_vouchers(self):
        if input("Send vouchers to {} registered without membership people? (y/n) ".format(len(self.registered_without_membership_csv))) != 'y':
            return
        self.create_vouchers(self.registered_without_membership_csv)

    def create_vouchers(self, targets):
        return [self.create_voucher(t) for t in targets]

    def create_voucher(self, target):
        quota = self.quota
        if target["low_income"]:
            quota = self.low_income_quota
        voucher = self.pretix.create_voucher(quota,
                                             block_quota=False,
                                             tag="fcfs",
                                             comment=json.dumps(target, indent=2),
                                             valid_until=datetime.now()+timedelta(hours=180))
        if not voucher:
            raise RuntimeError("Unable to create voucher")
        self.send_voucher(target, voucher)
        print("sent voucher {}".format(voucher))
        return voucher

    def send_voucher(self, target, voucher):
        self.pretix.send_email(to=[target["email"]],
                               subject="Welcome to the Open Membership sale 🦅",
                               body="""
Hello there,

Most of the memberships have been sold by now to the winners of the lottery and their plus ones, however, there are still <XXX> memberships left, and this may be your chance to get yours!

Yes, you read it right: you still have a chance to get a membership! 

Follow this link and purchase a membership until we run out.   

https://{}/{}/{}/redeem?voucher={}

Bleeps and Bloops,


The Membership Team 🤖
""".format(self.pretix.host, self.pretix.org, self.pretix.event,
           voucher["code"]))

    def load_csv(self):
        try:
            with open(self.csvfile, newline='', encoding="utf8") as c:
                r = list(csv.DictReader(c))
        except FileNotFoundError:
            print("Creating new file ...")
            r = []
        return r

    def save_csv(self):
        with open(self.csvfile, 'w', newline='', encoding="utf8") as c:
            if len(self.registered_without_membership_csv) > 0:
                print(f"Saved {len(self.registered_without_membership_csv)} member(s) on file '{self.csvfile}'")
                fieldnames = self.registered_without_membership_csv[0].keys()
                writer = csv.DictWriter(c, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.registered_without_membership_csv)
