class TransferTool:
    def __init__(self, pretix):
        self.pretix = pretix

    def display(self):
        print(self.pretix.get_refund_requests())

    def update(self):
        self.pretix.update_refund_request(1, "i")

    # SMEP:
    # User creates request
    # if voucher is used and order is not refunded -> refund
    # else if voucher is NULL or expired and quota is full -> generate voucher

    # Transfer:
    # User creates request
    # if voucher is used and order is not refunded -> refund
    # else if voucher is null and request is authorized -> generate voucher

