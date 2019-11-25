#!/usr/bin/env python3 -w

# +1 Replication

# TODO
# add an option to filter orders by voucher tag - e.g. only do those from lottery!
# Send email
# get correct quota group
# getopts/tool
# warn about missing env stuff - there might actually be enough variables here to warrant a config file

from os import getenv
from pretix import PretixAPI
import json

quota_group = 1 # TODO
invite_identifier = getenv("INVITE_ID", "ZAGGLL3V")
prefname_identifier = getenv("PREFNAME_ID", "prefname")

pretix = PretixAPI(token="2wxpbi0bwubye1w6z9kq7qd33hoz9svgjq1i4s0xi2e4mfiucnwcehnep8vns4e5")

def replicate():
    already_invited = list(get_already_used_orders())
    invites = list(get_order_invitations())

    print("{} invitations pending.".format(len(invites)-len(already_invited)))

    for inviteinfo in invites:
        if inviteinfo["invited_by_order"] in already_invited:
            continue
        if not create_invitation(inviteinfo):
            print("Creating invitation failed. Assuming quota is full. Bye!")
            break

def create_invitation(inviteinfo):
    voucher = pretix.create_voucher(quota = quota_group,
                                    comment = json.dumps(inviteinfo,
                                                         indent=2))
    if voucher:
        print(voucher['code'])
        # send email
        return True
    return False

def get_order_invitations():
    invites = map(get_inviteinfo_from_order,
                  pretix.get_orders())
    return filter(None, invites)

def get_inviteinfo_from_order(order):
    invited = get_answer_from_order(order, invite_identifier)
    prefName = get_answer_from_order(order, prefname_identifier)
    return { "email": invited,
             "invited_by_email": order['email'],
             "invited_by_name": prefName,
             "invited_by_order": order['code'],
             "datetime": order['datetime'] }

def get_answer_from_order(order, identifier):
    answer = [ a for a in order['positions'][0]['answers']
               if a['question_identifier'] == identifier ]
    if answer:
        return answer[0]['answer']
    return None

def get_already_used_orders():
    return filter(None,
                  map(get_invite_orders_from_voucher,
                      pretix.get_vouchers()))

def get_invite_orders_from_voucher(voucher):
    try:
        inviteinfo = json.loads(voucher['comment'])
    except json.JSONDecodeError:
        return None
    return inviteinfo.get('invited_by_order', None)

if __name__ == "__main__":
    replicate()

