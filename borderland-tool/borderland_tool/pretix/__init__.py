from requests import post, get, patch
from datetime import datetime, timedelta
import sys
import math


class PretixAPI:
    def __init__(self, host, org, event, token, no_ssl=False):
        self.host = host
        self.org = org
        self.event = event
        self.token = token
        self.url_scheme = "https"
        if no_ssl:
            self.url_scheme = "http"
        self.url = "url_init_value"
        self.dryrun = False

    def set_dry_run(self):
        self.dryrun = True

    def get_orders(self, status="p"):
        self.url = f"{self.url_scheme}://{self.host}/api/v1/organizers/{self.org}/events/{self.event}/orders/?page=1"
        return self.get_paginated(self.url,
                                  json={"ordering": "datetime",
                                        "status": status})

    def get_vouchers(self):
        self.url = f"{self.url_scheme}://{self.host}/api/v1/organizers/{self.org}/events/{self.event}/vouchers/?page=1"
        return self.get_paginated(self.url, {})

    def patch_voucher(self, vid, updates):
        self.url = f"{self.url_scheme}://{self.host}/api/v1/organizers/{self.org}/events/{self.event}/vouchers/{vid}/"
        if self.dryrun:
            return
        resp = patch(self.url,
                     headers={"Authorization": "Token {}".format(self.token)},
                     json=updates)
        if resp.status_code > 299:
            print(resp.text)
            return None
        return resp.json()

    def create_voucher(self,
                       quota,
                       comment="",
                       block_quota=True,
                       tag="replication",
                       valid_until=datetime.now()+timedelta(hours=1)):
        self.url = f"{self.url_scheme}://{self.host}/api/v1/organizers/{self.org}/events/{self.event}/vouchers/"
        if self.dryrun:
            return
        resp = post(self.url,
                    headers={"Authorization": "Token {}".format(self.token)},
                    json={"comment": comment,
                          "block_quota": block_quota,
                          "valid_until": str(valid_until),
                          "tag": tag,
                          "quota": quota})
        if resp.status_code != 201:
            print(resp.text)
            return None
        return resp.json()

    # get quota
    # get quota_availability

    ### Borderland plugin

    # TODO make own class
    def get_refund_requests(self):
        url = f"{self.url_scheme}://{self.host}/api/v1/organizers/{self.org}/events/{self.event}/refund/"
        return self.get_paginated(url, {})

    def update_refund_request(self, id, status):
        url = f"{self.url_scheme}://{self.host}/api/v1/organizers/{self.org}/events/{self.event}/refund/{id}/"
        if self.dryrun:
            return
        resp = patch(url,
                    headers = { "Authorization": "Token {}".format(self.token) },
                    json = { "status": status })
        if resp.status_code != 200:
            print(resp.text)
            raise RuntimeError("Pretix returned status code {} for {} with {}".format(resp.status_code, url, json))
        return resp.json()

    def get_registrations(self):
        self.url = f"{self.url_scheme}://{self.host}/api/v1/organizers/{self.org}/events/{self.event}/registration/"
        return self.get_paginated(self.url, {})

    def get_registrations_without_membership(self):
        url = f"{self.url_scheme}://{self.host}/api/v1/organizers/{self.org}/events/{self.event}/registration?without-membership=true"
        return self.get_paginated(url, {})

    def send_email(self, to, subject, body):
        url = f"{self.url_scheme}://{self.host}/api/v1/organizers/{self.org}/events/{self.event}/email/"
        resp = post(url,
                    headers = { "Authorization": "Token {}".format(self.token) },
                    json = { "to": to, "subject": subject, "body": body })
        if resp.status_code != 200:
            print(resp.text)
            raise RuntimeError("Pretix returned status code {} for {}".format(resp.status_code, url))



    # Internal

    def get_paginated(self, url, json):
        print("get_paginated, self.dryrun={}".format(self.dryrun))
        if self.dryrun:
            return []
        results = []
        next_url = url
        count = 1
        while next_url:
            sys.stderr.write("\rLoading {}: {}% complete".format(url, math.floor(100.0* len(results)/count)))
            resp = get(next_url,
                headers = { "Authorization": "Token {}".format(self.token) },
                json = json)
            if resp.status_code >= 300:
                print(resp.text)
                raise RuntimeError("Pretix returned status code {} for {} with {}".format(resp.status_code, url, json))
            resp_json = resp.json()
            results += resp_json['results']
            next_url = resp_json['next'] # !
            count = resp_json['count']
        sys.stderr.write("\r\n")
        return results

