from requests import post, get, put, patch
from datetime import datetime, timedelta

class PretixAPI:
    def __init__(self, host, org, event, token):
        self.host = host
        self.org = org
        self.event = event
        self.token = token


    def get_orders(self, status="p"):
        url = "http://{}/api/v1/organizers/{}/events/{}/orders/?page=1".format(self.host, self.org, self.event)
        return self.get_paginated(url,
                                  json = { "ordering": "datetime",
                                           "status": status })


    def get_vouchers(self):
        url = "http://{}/api/v1/organizers/{}/events/{}/vouchers/?page=1".format(self.host, self.org, self.event)
        return self.get_paginated(url, {})


    def create_voucher(self,
                       quota,
                       comment="",
                       block_quota=True,
                       tag="replication",
                       valid_until=str(datetime.now()+timedelta(days=2))):
        url = "http://{}/api/v1/organizers/{}/events/{}/vouchers/".format(self.host, self.org, self.event)
        resp = post(url,
                    headers = { "Authorization": "Token {}".format(self.token) },
                    json = { "comment": comment,
                             "block_quota": block_quota,
                             "valid_until": valid_until,
                             "tag": tag,
                             "quota": quota })
        if resp.status_code != 201:
            print(resp.text)
            return None
        return resp.json()

    # get quota
    # get quota_availability

    ### Borderland plugin

    # TODO make own class
    def get_refund_requests(self):
        url = "http://{}/api/v1/organizers/{}/events/{}/refund/".format(self.host, self.org, self.event)
        return self.get_paginated(url, {})

    def update_refund_request(self, id, status):
        url = "http://{}/api/v1/organizers/{}/events/{}/refund/{}/".format(self.host, self.org, self.event, id)
        resp = patch(url,
                    headers = { "Authorization": "Token {}".format(self.token) },
                    json = { "status": status })
        if resp.status_code != 200:
            print(resp.text)
            raise RuntimeError("Pretix returned status code {} for {} with {}".format(resp.status_code, url, json))
        return resp.json()


    def get_registrations(self):
        url = "http://{}/api/v1/organizers/{}/events/{}/registration/".format(self.host, self.org, self.event)
        return self.get_paginated(url, {})

    # Internal

    def get_paginated(self, url, json):
        results = []
        next_url = url
        while next_url:
            resp = get(next_url,
                headers = { "Authorization": "Token {}".format(self.token) },
                json = json)
            if resp.status_code >= 300:
                print(resp.text)
                raise RuntimeError("Pretix returned status code {} for {} with {}".format(resp.status_code, url, json))
            resp_json = resp.json()
            results += resp_json['results']
            next_url = resp_json['next'] # !
        return results

