import json


def get(context, url):
    print("GET " + url)
    r = context.request(url, "GET", "")
    if r["status"] < 200 or r["status"] > 299:
        raise Exception('HTTP error %d: %s' % (r["status"], r["content"]))
    return json.loads(r["content"])


def post(context, url, data):
    print("POST " + url)
    r = context.request(url, "POST", json.dumps(data))
    if r["status"] < 200 or r["status"] > 299:
        raise Exception('HTTP error %d: %s' % (r["status"], r["content"]))
    return json.loads(r["content"])


def handler(context, inputs):
    dep_id = inputs["deploymentId"]

    # Un-tag the network as suitable for this VM
    for subnet in inputs["subnetIds"]:
        tags = get(context, "/iaas/api/fabric-networks/" + subnet).get("tags", [])
        print("Original tags: " + str(tags))
        to_delete = list(filter(lambda t: t["key"] == "__fitsResource" or not t["value"].startswith(dep_id), tags))
        payload = {
            "resourceLink": "/resources/sub-networks/" + subnet,
            "tagsToAssign": [],
            "tagsToUnassign": to_delete
        }
        post(context, "/provisioning/uerp/provisioning/mgmt/tag-assignment", payload)
        print("Deleted tags: " + str(to_delete))
