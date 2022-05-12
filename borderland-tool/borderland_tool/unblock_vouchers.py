#!/usr/bin/env python3

from borderland_tool.get_pretix import get_pretix
from borderland_tool.voucher import Voucher


def unblock_vouchers(args):
    pretix = get_pretix(args)
    vouchers = sum(args.vouchers, [])
    voucher = Voucher(pretix)
    if len(vouchers) > 0:
        voucher.unblock(vouchers)
    else:
        voucher.unblock_all()
