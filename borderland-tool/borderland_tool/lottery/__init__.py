#!/usr/bin/python3
import csv
import random
import json

from datetime import datetime, timezone, timedelta
from dateutil import parser


class Lottery:
    def __init__(self, pretix, csvfile, quota):
        self.pretix = pretix
        self.csvfile = csvfile
        self.quota = quota
        self.registrations_csv = self.load_csv()
        self.has_order = self.has_voucher = None

    def registrations_to_csv(self):
        """Retrieve registered users from Pretix plugin and update CSV"""
        registrations_pretix = self.pretix.get_registrations()
        if self.registrations_csv:
            last = int(self.registrations_csv[-1]['id'])
        else:
            last = -1
        new_registrations = [
            r for r in registrations_pretix if int(r['id']) > last]
        print("{} new registrations found".format(len(new_registrations)))
        for r in new_registrations:
            print(f'{r["email"]}: {r["first_name"]} {r["last_name"]}')
        self.registrations_csv = self.registrations_csv + new_registrations
        self.save_csv()

    def losers(self):
        self.load_orders_and_vouchers()
        eligible = [
            r for r in self.registrations_csv if self.is_eligible(r["email"])]
        print(", ".join([e["email"] for e in eligible]))
        print(len(eligible))
        if input("Send sad email (2022 specific text!)? (y/n) ") != 'y':
            return
        for target in eligible:
            self.pretix.send_email(to=[target["email"]],
                                   subject="So, you didn't win the Borderland lottery 😭",
                                   body="""Hello from memberships HQ. It's time to cry.

It's an inevitable fact that Borderland grows in popularity faster than we can create the organizational knowledge to host a bigger event.

It's incredibly sad and unfair to have to say no to any single one of you. But sometimes facts are unfair, even in the land between dreams and reality.

All hope is not lost though, as many memberships tend to change hands as the event grows
closer and summer plans change. Also, anyone who won the lottery has the chance to invite a +1 (so now you know who to flirt with). Maybe you’ll find a way to get your membership!

Bleeps and Bloops,

The Borderland Understaffed Tech Team 🤖
""")
            print("Emailt {}" + target["email"])

    def lottery(self, num):
        winners = self.raffle(num)
        print([w["email"] for w in winners])
        if input("Drew {} winners! Send invitations? (y/n) ".format(len(winners))) != 'y':
            return
        self.create_vouchers(winners)

    def raffle(self, num):
        eligible = [
            r for r in self.registrations_csv if self.is_eligible(r["email"])]
        random.shuffle(eligible)
        return eligible[:num]

    def create_vouchers(self, targets):
        return [self.create_voucher(t) for t in targets]

    def create_voucher(self, target):
        voucher = self.pretix.create_voucher(self.quota,
                                             tag="lottery",
                                             comment=json.dumps(target, indent=2),
                                             valid_until=datetime.now()+timedelta(hours=48))
        if not voucher:
            raise RuntimeError("Unable to create voucher")
        self.send_voucher(target, voucher)
        print("sent voucher {}".format(voucher))
        return voucher

    def send_voucher(self, target, voucher):
        self.pretix.send_email(to=[target["email"]],
                               subject="You're invited to The Borderland 2022! 🔥",
                               body="""
Wow, you won the Borderland lottery! You hereby can purchase a membership for the Borderland, and to invite a friend of your choice to purchase their membership!

Follow this link to purchase your membership! It's valid for 48 hours.

https://{}/{}/{}/redeem?voucher={}

Please note that this is a ~special~ lottery invitation. This means you have to use the same name and birth date as when you registered. For reference, the information you provided was:

  * First Name: {}
  * Last Name: {}
  * Date of Birth: {}

The second voucher you receive is not personal and can be sent to a friend of your choice, so that they may get the possibility to purchase a membership! This can be anyone really, but try to reflect on who would contribute to the co-created event, and/or who would get out a lot from going. This gift voucher has the same 48 hours limit as your original voucher.

Bleeps and Bloops,

The Borderland Understaffed Tech Team 🤖
""".format(self.pretix.host, self.pretix.org, self.pretix.event,
           voucher["code"], target["first_name"], target["last_name"],
           target["dob"]))  # TODO show validity from voucher

    def is_eligible(self, email):
        self.load_orders_and_vouchers()
        # Eligible if email doesn't already have an order or a valid voucher
        return email not in self.has_order and email not in self.has_voucher

    # def order_names_control()
    # check that order == voucher name == registration name

    def load_orders_and_vouchers(self):
        # Cache preexisting orders
        if not self.has_order:
            # TODO there's a wrong assumption in this strategy - users can just use a secondary email on their other
            # the right thing to do here is to include emails from vouchers that has been redeemed
            self.has_order = [o["email"]
                              for o in self.pretix.get_orders() if o['status'] == 'p']
        # Cache preexisting vouchers
        if self.has_voucher is None:
            self.has_voucher = []
            valids = [v for v in self.pretix.get_vouchers() if v['quota'] == self.quota and
                      v['redeemed'] < v['max_usages']]  # and
            # parser.parse(v['valid_until']) > datetime.now(timezone.utc) ]
            for v in valids:
                try:
                    comment = json.loads(v['comment'])
                    self.has_voucher += [comment["email"]]
                except:  # json.decoder.JSONDecodeError:
                    continue

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
            num_csv_registrations = len(self.registrations_csv)
            if num_csv_registrations > 0:
                fieldnames = self.registrations_csv[0].keys()
                print("found {} registered users".format(
                    num_csv_registrations))
            else:
                print("No registered users found")
            writer = csv.DictWriter(c, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.registrations_csv)
