#!/usr/bin/env python3

import get_pretix


def unblock_vouchers(args):
    from borderland_tool.voucher import Voucher
    pretix = get_pretix(args)
    vouchers = sum(args.vouchers, [])
    voucher = Voucher(pretix)
    if len(vouchers) > 0:
        voucher.unblock(vouchers)
    else:
        voucher.unblock_all()
