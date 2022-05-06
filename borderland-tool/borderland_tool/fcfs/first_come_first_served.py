#!/usr/bin/python3
import csv
import random
import json

from datetime import datetime, timezone, timedelta
from dateutil import parser


class FCFS:
    def __init__(self, pretix, csvfile, quota):
        self.pretix = pretix
        self.csvfile = csvfile
        self.quota = quota
        self.registered_without_membership_csv = self.load_csv()
        self.has_order = self.has_voucher = None

    def registrations_to_csv(self):
        self.registered_without_membership_csv = self.pretix.get_registrations_without_membership()
        print("{} members registered to the lottery but did not have a membership".format(len(new_registrations)))
        self.save_csv()

    def send_vouchers(self, num):
        if input("Send vouchers to {} registered without membership people? (y/n) ".format(len(self.registered_without_membership_csv))) != 'y':
            return
        self.create_vouchers(self.registered_without_membership_csv)

    def create_vouchers(self, targets):
        return [self.create_voucher(t) for t in targets]

    def create_voucher(self, target):
        voucher = self.pretix.create_voucher(self.quota,
                                             block_quota=False,
                                             tag="fcfs",
                                             comment=json.dumps(target, indent=2),
                                             valid_until=datetime.now()+timedelta(hours=24))
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

You're receiving this email because you registered to the Borderland Grand Lottery and didn't win nor get invited by a friend.

No worries!, You still have a chance to get a membership! 

Follow this link and purchase a membership before we run out, there are 800 memberships left, so don't think twice and get yours!    

https://{}/{}/{}/redeem?voucher={}

Bleeps and Bloops,

The Borderland Understaffed Tech Team 🤖

PS: These vouchers expire in 24h and are not transferable.
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
            print("found {} registered without membership users".format(len(self.registered_without_membership_csv)))
            if len(self.registered_without_membership_csv) > 0:
                fieldnames = self.registered_without_membership_csv[0].keys()
                writer = csv.DictWriter(c, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.registered_without_membership_csv)
