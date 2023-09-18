import unittest
import testsupport
import yaml
import os

from src.main.python.nwselect import main as nwselect


class TestIPRange(testsupport.MyTest):
    def __init__(self, name):
        super().__init__(name)

    def test_getiprange(self):
        inputs = { "ipamUser": "admin", "ipamPassword": "VMware1!", "ipamHost": "infoblox.sof-mbu.eng.vmware.com"}
        nwselect.get_available_ips(self.context, inputs, "8fc93e0b-2371-4684-8d19-0c7002d99a28")

    def test_handler(self):
        payload = {
            "tags": {},
            "target": "World",
            "zoneId": "f65d18c2-9e5d-4fad-9474-5ca2a81b97e5",
            "projectId": "54fc4d37-f1a8-446e-bdfd-d29ef4ffd922",
            "requestId": "6826e0da-7142-445c-8c53-f9192467596a",
            "__metadata": {
                "orgId": "be0c4536-a922-46d2-9857-f824ecc6ac9c",
                "headers": {
                    "tokenId": "f+N7uAuMFnoA8QgC9FykmpCM8oGyC0sZm1AXU7wUik4=",
                    "blocking": "true",
                    "runnableId": "1232c505-5468-4952-a4fe-e375ac46c871",
                    "runnableType": "extensibility.abx",
                    "uber-trace-id": "ecfa7560d68246c69e85fd61b0dcb724:a74ebb0c6cd64229855e0a7f97d750d4:f096bf49-3d76-4b84-9b8b-2ee6446c365f:1",
                    "uberctx-org-id": "be0c4536-a922-46d2-9857-f824ecc6ac9c",
                    "uberctx-user-id": "provisioning-jyY9lurLjBFQDbBl",
                    "eventTraceEntryId": "973d00d1-59cf-4349-837a-d2776efedc54",
                    "sampling-decision": "true",
                    "uberctx-parent-id": "f096bf49-3d76-4b84-9b8b-2ee6446c365f",
                    "encryption-context": "52dd45d5-8937-413e-b488-208abba21c5a",
                    "uberctx-serviceurl": "http://10.244.0.22:8282/provisioning/requests/compute-allocation-tasks/b02c9b9e-9351-4fe7-9568-9a41554bbeec",
                    "uberctx-request-trace-id": "36d8150f-26a9-439e-b050-94f0a432ef2f",
                    "provisioning-callback-uri": "/provisioning/config/extensibility-callbacks/7dd2f3c9-7a09-3f25-afdf-be17856cf0b8"
                },
                "targetId": "b02c9b9e-9351-4fe7-9568-9a41554bbeec",
                "userName": "fritz",
                "eventType": "EVENT",
                "timeStamp": 1651851954372,
                "sourceType": "provisioning",
                "targetType": "ComputeAllocationTaskState",
                "eventTopicId": "network.configure",
                "correlationId": "52dd45d5-8937-413e-b488-208abba21c5a--6826e0da-7142-445c-8c53-f9192467596a",
                "sourceIdentity": "12a7739c-77a7-4566-a2ba-9474762469a6",
                "correlationType": "contextId"
            },
            "endpointId": "454dcc86-e855-464a-b976-982263859f31",
            "blueprintId": "34c2d6f5-2bb3-4f27-ba1d-d6cad84f07c1",
            "componentId": "Cloud_vSphere_Machine_1[0]",
            "externalIds": [
                "Cloud_vSphere_Machine_1-mcm449-200245552856",
                "Cloud_vSphere_Machine_1-mcm450-200245552856",
                "Cloud_vSphere_Machine_1-mcm451-200245552856"
            ],
            "resourceIds": [
                "d030cfba-ad84-4edc-b7c2-57ce16602566",
                "4a837351-15d0-4e42-9f06-10a7b6b773e4",
                "4b175622-3356-4d65-b3b6-f97855467b82"
            ],
            "deploymentId": "52dd45d5-8937-413e-b488-208abba21c5a",
            "componentTypeId": "Cloud.vSphere.Machine",
            "customProperties": {
                "count": "3",
                "image": "Linux",
                "project": "54fc4d37-f1a8-446e-bdfd-d29ef4ffd922",
                "zone_overlapping_migrated": "true"
            },
            "networkProfileIds": [
                "4251b92a-23ea-4dc8-a4c0-f9a6b1cc029a",
                "4251b92a-23ea-4dc8-a4c0-f9a6b1cc029a",
                "4251b92a-23ea-4dc8-a4c0-f9a6b1cc029a"
            ],
            "networkSelectionIds": [
                [
                    [
                        "edb68802-fb48-4770-8200-1b4f09fc9ccf",
                        "037c7a81-7392-4785-bc7b-63356a4a2251",
                        "2fa13be3-23a0-4c09-a172-11749ba7b49b",
                        "8002a055-6b2f-464e-ad21-c430110a2150"
                    ],
                    [
                        "edb68802-fb48-4770-8200-1b4f09fc9ccf",
                        "037c7a81-7392-4785-bc7b-63356a4a2251",
                        "2fa13be3-23a0-4c09-a172-11749ba7b49b",
                        "8002a055-6b2f-464e-ad21-c430110a2150"
                    ],
                    [
                        "edb68802-fb48-4770-8200-1b4f09fc9ccf",
                        "037c7a81-7392-4785-bc7b-63356a4a2251",
                        "2fa13be3-23a0-4c09-a172-11749ba7b49b",
                        "8002a055-6b2f-464e-ad21-c430110a2150"
                    ]
                ],
                [
                    [
                        "edb68802-fb48-4770-8200-1b4f09fc9ccf",
                        "037c7a81-7392-4785-bc7b-63356a4a2251",
                        "2fa13be3-23a0-4c09-a172-11749ba7b49b",
                        "8002a055-6b2f-464e-ad21-c430110a2150"
                    ],
                    [
                        "edb68802-fb48-4770-8200-1b4f09fc9ccf",
                        "037c7a81-7392-4785-bc7b-63356a4a2251",
                        "2fa13be3-23a0-4c09-a172-11749ba7b49b",
                        "8002a055-6b2f-464e-ad21-c430110a2150"
                    ],
                    [
                        "edb68802-fb48-4770-8200-1b4f09fc9ccf",
                        "037c7a81-7392-4785-bc7b-63356a4a2251",
                        "2fa13be3-23a0-4c09-a172-11749ba7b49b",
                        "8002a055-6b2f-464e-ad21-c430110a2150"
                    ]
                ],
                [
                    [
                        "edb68802-fb48-4770-8200-1b4f09fc9ccf",
                        "037c7a81-7392-4785-bc7b-63356a4a2251",
                        "2fa13be3-23a0-4c09-a172-11749ba7b49b",
                        "8002a055-6b2f-464e-ad21-c430110a2150"
                    ],
                    [
                        "edb68802-fb48-4770-8200-1b4f09fc9ccf",
                        "037c7a81-7392-4785-bc7b-63356a4a2251",
                        "2fa13be3-23a0-4c09-a172-11749ba7b49b",
                        "8002a055-6b2f-464e-ad21-c430110a2150"
                    ],
                    [
                        "edb68802-fb48-4770-8200-1b4f09fc9ccf",
                        "037c7a81-7392-4785-bc7b-63356a4a2251",
                        "2fa13be3-23a0-4c09-a172-11749ba7b49b",
                        "8002a055-6b2f-464e-ad21-c430110a2150"
                    ]
                ]
            ]
        }
        nwselect.handler(self.context, payload)

    def test_get_networks(self):
        networks = nwselect.get_networks(self.context, "e768bd7c-c8d2-4d1d-acb8-8ceee5ae4fba", "Cloud_Machine_1")
        print(networks)