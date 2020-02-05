from datetime import datetime
from dateutil.parser import parse

class Voucher:
    def __init__(self, pretix):
        self.pretix = pretix
        self.vouchers = pretix.get_vouchers()


    def voucher_id_for_code(self, vcode):
        matches = [ v['id'] for v in self.vouchers if v['code'] == vcode ]
        if matches != []:
            return matches[0]
        else:
            print(vcode)
            return 0

    def unblock(self, vcodes):
        for vcode in vcodes:
            print(self.pretix.patch_voucher(self.voucher_id_for_code(vcode), {
              "valid_until": None,
              "block_quota": False
            }))


    def unblock_all(self):
        vouchers = [ v['code'] for v in self.vouchers if v['redeemed'] == 0 and v['valid_until'] and parse(v['valid_until'], ignoretz=True) < datetime.utcnow() ]
        return self.unblock(vouchers)

