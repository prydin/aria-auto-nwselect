import json
import requests
import uuid
import yaml
from functools import reduce

MAX_USAGE = 100


def get(context, url):
    r = context.request(url, "GET", "")
    if r["status"] < 200 or r["status"] > 299:
        raise Exception('HTTP error %d: %s' % (r["status"], r["content"]))
    return json.loads(r["content"])


def ip_to_int(ip):
    total = int(0)
    for n in ip.split('.'):
        total = (total << 8) + int(n)
    return total


cache = {}


def get_available_ips(context, subnet):
    n = cache.get(subnet, None)
    if n:
        return n
    total = 0
    used = 0

    # Loop over all ranges defined for this subnet
    ipRangeEnvelope = get(context,
                          "/provisioning/uerp/provisioning/mgmt/subnet-range?expand&$filter=(subnetLink%20eq%20%27%2Fresources%2Fsub-networks%2F" + subnet + "%27)&top=20&$orderby=name%20asc&$skip=0")
    for ipRange in ipRangeEnvelope['documents'].values():
        startIp = ip_to_int(ipRange['startIPAddress'])
        endIp = ip_to_int(ipRange['endIPAddress'])
        total += endIp - startIp
        rangeLink = ipRange['documentSelfLink']

        # Count the IPs that are used in this range
        ips = get(context,
                  "/provisioning/uerp/provisioning/mgmt/ip-address?expand&$filter=((subnetRangeLink%20eq%20%27" + rangeLink + "%27)%20and%20(ipAddressStatus%20ne%20%27*AVAILABLE*%27))&$orderby=name%20asc&$top=10&$skip=0")
        used += ips['totalCount']
    n = total - used
    cache[subnet] = n
    return n


def handler(context, inputs):
    outputs = inputs

    # Preselect the network with the most available IPs
    vms = outputs['networkSelectionIds']
    print(vms)
    for vm_idx in range(len(vms)):
        vm = vms[vm_idx]
        # Get the number of private network NICs. They need some special handling. NB: This will only
        # work if private networks are always the LAST elements in the network list on a VM!
        res_id = inputs["resourceIds"][vm_idx]
        dep_id = inputs["deploymentId"]
        deployment = get(context, "/deployment/api/deployments/%s?expand=resources" % dep_id)
        num_networks = 0
        print(deployment["resources"])
        for resource in deployment["resources"]:
            if resource["type"].endswith(".Network"):
                num_networks += 1
                print(get(context, "/deployment/api/deployments/%s/resources/%s" % (dep_id, resource["id"])))
        print("Found %d networks in deployment. Inputs has %d networks" % (num_networks, len(vm)))

        for subnet in vm:
            best_subnet = reduce(lambda a, b: a if get_available_ips(context, a) > get_available_ips(context, b) else b,
                                 subnet)
            subnet[:] = [best_subnet]
            print("Best subnet is %s with %d free IPs" % (best_subnet, get_available_ips(context, best_subnet)))

        # Pad empty selections for on-demand networks
        for _ in range(num_networks - len(vm)):
            vm.append([])

    print(json.dumps(inputs['networkSelectionIds']))
    return outputs
