#!/usr/bin/env python3 -w

# +1 Replication

import json
from datetime import datetime, timedelta

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
        self.pretix = pretix


    def replicate(self, force=False):
        invites = self.invites_to_send()

        for i in invites:
            print("{} invites {}".format(i['invited_by_name'], i['email']))

        if len(invites) == 0:
            print('No new invites')
            return

        if not force and input("Continue? (y/n) ").lower().strip() != "y":
            print("User aborted.")
            return

        for inviteinfo in invites:
            if not self.create_invitation(inviteinfo):
                print("Creating invitation failed. Assuming quota is full. Bye!")
                break


    def invites_to_send(self):
        already_invited = list(self.get_already_used_orders())
        invites = list(self.get_order_invitations())

        return [ invite for invite in invites
                 if invite["invited_by_order"] not in already_invited and
                 invite["email"] and
                 self.voucher_id_has_allowed_tag(invite["invited_by_voucherids"]) ]


    def voucher_id_has_allowed_tag(self, ids):
        if self.allowed_voucher_tags == None:
            return True
        id_to_tag = { v['id']: v['tag'] for v in self.vouchers }
        invite_tags = [ id_to_tag[v] for v in ids if v != None ]
        intersect = set(invite_tags) & set(self.allowed_voucher_tags)
        if len(intersect) > 0:
            return True
        return False


    def create_invitation(self, inviteinfo):
        voucher = self.pretix.create_voucher(quota = self.quota_group,
                                             comment = json.dumps(inviteinfo, indent=2),
                                             valid_until=datetime.now()+timedelta(hours=48))
        if voucher:
            self.send_invitation(voucher, inviteinfo)
            return True
        return False


    def send_invitation(self, voucher, inviteinfo):
        self.pretix.send_email(to = [inviteinfo["email"]],
                               subject = "You've been invited to The Borderland 2022! 🔥",
                               body = """
Wow, {} must really like you! They've invited you to purchase a membership for the Borderland!

Follow this link to get yours! It's valid for 48 hours.

https://{}/{}/{}/redeem?voucher={}

This invitation is not personal, so you can pass it on if you like. It only works once though!
You can read more about the Borderland at https://theborderland.se/

The voucher is valid for 48 hours from the time it was sent to {}.

Bleeps and Bloops,

The Borderland Understaffed Tech Team 🤖
""".format(inviteinfo["invited_by_name"].split()[0].capitalize(),
           self.pretix.host, self.pretix.org, self.pretix.event,
           voucher["code"],
           inviteinfo["email"])) # TODO validity from voucher



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

    def get_orders_for_voucher(self, voucher_id):
        result = []
        for order in self.orders:
            for pos in order['positions']:
                if pos['voucher'] == voucher_id:
                    result += [order]
        return result

    def vizualise(self):
        # voucher that are redeemed
        redeemed = [ v for v in self.vouchers if v['redeemed'] > 0 ]
        # get preferred name for vouchers -> list of node labels
        nodes = []
        for voucher in redeemed:
            orders = self.get_orders_for_voucher(voucher['id'])
            for order in orders:
                nodes += [ {"id": voucher['id'], "label": self.get_answer_from_order(order, self.prefname_identifier) } ]
        # edges:
        # if tag == lottery, lottery -> id
        edges = [ {"from": "lottery", "to": v['id'] } for v in redeemed if v['tag'] == 'lottery' ]
        # if tag other: try to get comments, comments.invited_by_id -> id
        for voucher in [ v for v in redeemed if v['tag'] != 'lottery' ]:
            iinfo = self.get_inviteinfo_from_voucher(voucher)
            if iinfo and 'invited_by_voucherids' in iinfo:
                for fromid in iinfo['invited_by_voucherids']:
                    if fromid:
                        edges += [ { "from": fromid, "to": voucher['id'] } ]
        result = "digraph {\n"
        for node in nodes:
            result += "{} [label=\"{}\"];\n".format(node['id'], (node['label'] or "").replace('"', '\"'))
        for edge in edges:
            result += "{} -> {};\n".format(edge['from'], edge['to'])
        result += "}\n"
        return result




