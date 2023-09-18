import unittest

import requests
import yaml
import os


def read_configuration(filename):
    with open(filename, 'r') as stream:
        return yaml.safe_load(stream)


class FakeContext:
   #  hostname = "cava-216-125-29.eng.vmware.com"
    hostname = "cava-216-120-75.eng.vmware.com"

    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    def __init__(self, refresh_token):
        payload = {"refreshToken": refresh_token}
        response = requests.post(
            "https://%s/iaas/api/login" % self.hostname,
            json=payload,
            headers=self.headers,
            verify=False,
        )
        self.headers["Authorization"] = "Bearer " + response.json()["token"]

    def request(self, url, method, payload):
        r = requests.request(
            method,
            "https://%s%s" % (self.hostname, url),
            data=payload,
            headers=self.headers,
            verify=False,
        )
        return {"status": r.status_code, "content": r.content.decode("utf-8")}

    def getSecret(self, secret):
        return secret


class MyTest(unittest.TestCase):
    def __init__(self, name):
        super().__init__(name)
        self.config = read_configuration(os.getenv("TEST_CONFIG"))
        self.context = FakeContext(self.config["vraToken"])
