import unittest
import testsupport
import yaml
import os

from src.main.python.cleanup import main as cleanup


class TestCleanup(testsupport.MyTest):
    def __init__(self, name):
        super().__init__(name)

    def test_cleanup(self):
        payload = {
            "deploymentId": "b088c5eb-22b2-4a98-ba68-d068ed2612aa",
            "subnetIds": [
                "62cee44d-78c0-4ff0-be48-e1a759a05aa5"
            ]
        }
        cleanup.handler(self.context, payload)