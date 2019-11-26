#!/usr/bin/env python3 -w

# +1 Replication

# TODO
# Send email

from os import getenv
import json


class VoucherReplicator:
    def __init__(self,
                 pretix,
                 allowed_voucher_tags,
                 quota_group,
                 invite_identifier,
                 prefname_identifier):
        self.vouchers = pretix.get_vouchers()
        self.orders = pretix.get_orders()
        self.allowed_voucher_tags = allowed_voucher_tags
        self.quota_group = quota_group # TODO using internal id is cumbersome
        self.invite_identifier = invite_identifier
        self.prefname_identifier = prefname_identifier


    def replicate(self, force=False):
        already_invited = list(self.get_already_used_orders())
        invites = list(self.get_order_invitations())

        print("{} invitations pending.".format(len(invites)-len(already_invited)))

        # TODO more info here

        if not force and input("Continue? (y/n) ").lower().strip() != "y":
            print("User aborted.")
            return

        for inviteinfo in invites:
            if inviteinfo["invited_by_order"] in already_invited:
                continue
            if not self.voucher_id_has_allowed_tag(inviteinfo["invited_by_voucherids"]):
                continue
            if not self.create_invitation(inviteinfo):
                print("Creating invitation failed. Assuming quota is full. Bye!")
                break


    def voucher_id_has_allowed_tag(self, ids):
        if not self.allowed_voucher_tags:
            return True
        id_to_tag = { v['id']: v['tag'] for v in self.vouchers }
        invite_tags = [ id_to_tag[v] for v in ids ]
        intersect = set(invite_tags) & set(self.allowed_voucher_tags)
        if len(intersect) > 0:
            return True
        return False


    def create_invitation(self, inviteinfo):
        voucher = pretix.create_voucher(quota = self.quota_group,
                                        comment = json.dumps(inviteinfo,
                                                            indent=2))
        if voucher:
            print(voucher['code'])
            # send email
            return True
        return False


    def get_order_invitations(self):
        invites = map(self.get_inviteinfo_from_order, self.orders)
        return filter(None, invites)


    def get_inviteinfo_from_order(self, order):
        invited = self.get_answer_from_order(order, self.invite_identifier)
        prefName = self.get_answer_from_order(order, self.prefname_identifier)
        return { "email": invited,
                 "datetime": order['datetime'],
                 "invited_by_email": order['email'],
                 "invited_by_name": prefName,
                 "invited_by_order": order['code'],
                 "invited_by_voucherids": [ p['voucher'] for p in order['positions'] ] }


    def get_answer_from_order(self, order, identifier):
        answer = [ a for a in order['positions'][0]['answers']
                if a['question_identifier'] == identifier ]
        if answer:
            return answer[0]['answer']
        return None


    def get_already_used_orders(self):
        return filter(None,
                    map(self.get_invite_orders_from_voucher,
                        self.vouchers))


    def get_invite_orders_from_voucher(self, voucher):
        inviteinfo = self.get_inviteinfo_from_voucher(voucher)
        if inviteinfo:
            return inviteinfo.get('invited_by_order', None)
        return None

    def get_inviteinfo_from_voucher(self, voucher):
        try:
            inviteinfo = json.loads(voucher['comment'])
        except json.JSONDecodeError:
            return None
        return inviteinfo
