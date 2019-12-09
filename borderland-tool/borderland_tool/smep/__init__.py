class TransferTool:
    def __init__(self, pretix):
        self.pretix = pretix

    def display(self):
        print(self.pretix.get_refund_requests())

    def update(self):
        self.pretix.update_refund_request(1, "i")

