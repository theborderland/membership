#!/usr/bin/python3
import csv
import random
import json

from datetime import datetime, timezone, timedelta
from dateutil import parser


class Lottery:
    def __init__(self, pretix, csvfile, quota, low_income_quota):
        self.pretix = pretix
        self.csvfile = csvfile
        self.quota = quota
        self.low_income_quota = low_income_quota
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
        if input("Send sad email (2024 specific text!)? (y/n) ") != 'y':
            return

        email = """
We know, it sucks. But some win, some lose. That's the rules of the game. 

It seems that The Borderland is growing in popularity faster than we can create the necessary cultural continuity and organizational capacity to host a bigger event.

It's incredibly sad and unfair to have to say no to any single one of you. But sometimes facts are unfair, even in the land between dreams and reality.

All hope is not lost, though, as anyone who won the lottery has the chance to invite a +1 (so now you know who to flirt with). Feel free to ask for it in a thread in the FB Borderland Memberships - Info & Support group. Also, not everyone who won will actually purchase a membership and not all of those who will purchase will offer +1 to someone.

That means that we will have a few hundred memberships left after the lottery concludes, and we will offer those on a first-come-first-serve basis to all those who registered for the lottery but lost - including you. Stay tuned - we will send you an email.

And even if you didn't get one by that time, know that many memberships tend to change hands as the dates closer to the Borderland and people's summer plans change. Who knows, maybe you'll find a way to get your membership transferred!

Stay strong,


The Membership Team 🤖
"""
        for target in eligible:
            self.pretix.send_email(to=[target["email"]],
                                   subject="Waah … you didn't win The Borderland lottery 😭",
                                   body=email)
            print(f"Email {target['email']}")

    def lottery(self, num):
        winners = self.raffle(num)
        print([w["email"] for w in winners])
        if input("Drew {} winners! Send invitations? (y/n) ".format(len(winners))) != 'y':
            return
        self.create_vouchers(winners)

    def raffle(self, num):
        eligible = [
            r for r in self.registrations_csv if self.is_eligible(r["email"])]
#        print("Registrations: {}".format(len(self.registrations_csv)))
#        print("Eligible: {}".format(len(eligible)))
        random.shuffle(eligible)
        return eligible[:num]

    def create_vouchers(self, targets):
        return [self.create_voucher(t) for t in targets]

    def create_voucher(self, target):
        quota = self.quota
        if eval(target["low_income"]):
            quota = self.low_income_quota

        voucher = self.pretix.create_voucher(quota,
                                             tag="lottery",
                                             comment=json.dumps(target, indent=2),
                                             valid_until=datetime.now() + timedelta(hours=72))
        if not voucher:
            raise RuntimeError("Unable to create voucher")
        self.send_voucher(target, voucher)
        print("sent voucher {}".format(voucher))
        return voucher

    def send_voucher(self, target, voucher):
        self.pretix.send_email(to=[target["email"]],
                               subject="You've won the lottery for Borderland 2024! 🔥",
                               body="""
Congratulations! You won The Borderland lottery! Hurray!🎉

You'll have the chance to acquire a membership and be amongst the first borderlings supporting The Borderland, yahoo!
And if that was peanuts ... you'll also have the chance to bring a friend/lover with you. Brilliant, isn't it? 

Follow this link to purchase your membership! It's valid for 72 hours.


https://{}/{}/{}/redeem?voucher={}


Please note that this is a *special* lottery invitation. This means you have to use the same name and birth date as when you registered. For reference, the information you provided was:

  * First Name: {}
  * Last Name: {}
  * Date of Birth: {}

Best regards on behalf of,


The Membership Team 🤖
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
            valids = [v for v in self.pretix.get_vouchers()
                      if v['quota'] == self.quota or
                      v['quota'] == self.low_income_quota and
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
