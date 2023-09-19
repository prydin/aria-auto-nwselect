import json
import time
from urllib.parse import quote
from functools import reduce
import requests
import requests.auth
import re
import yaml

DEBUG = False


def dump(data):
    print(json.dumps(data, indent=4))


def get(context, url):
    if DEBUG:
        print("GET", url, end="")
    t = time.time()
    r = context.request(url, "GET", "")
    if r["status"] < 200 or r["status"] > 299:
        raise Exception('HTTP error %d: %s' % (r["status"], r["content"]))
    if DEBUG:
        print(" (%fs)" % (time.time() - t))
    return json.loads(r["content"])


def patch(context, url, data):
    if DEBUG:
        print("PATCH", url, end="")
    t = time.time()
    r = context.request(url, "PATCH", json.dumps(data))
    if r["status"] < 200 or r["status"] > 299:
        raise Exception('HTTP error %d: %s' % (r["status"], r["content"]))
    if DEBUG:
        print(" (%fs)" % (time.time() - t))
    return json.loads(r["content"])


def post(context, url, data):
    if DEBUG:
        print("POST", url, end="")
    t = time.time()
    r = context.request(url, "POST", json.dumps(data))
    if r["status"] < 200 or r["status"] > 299:
        raise Exception('HTTP error %d: %s' % (r["status"], r["content"]))
    if DEBUG:
        print(" (%fs)" % (time.time() - t))
    return json.loads(r["content"])


def ip_to_int(ip):
    total = int(0)
    for n in ip.split('.'):
        total = (total << 8) + int(n)
    return total


def mkfilter(query):
    return "$filter=(" + quote(query, safe="*") + ")"


# Cache of IP counts. Used only during a single invocation
cache = {}


# Returns the number of free IP addresses based on IPAM data
def get_available_ips(context, inputs, subnet):
    n = cache.get(subnet, None)
    if n:
        return n

    # Loop over all ranges defined for this subnet
    ip_range_envelope = get(context,
                          '/provisioning/uerp/provisioning/mgmt/subnet-range?expand&' +
                          mkfilter("subnetLinks.item eq '/resources/sub-networks/%s'" % subnet) +
                          "&top=20&$orderby=name%20asc&$skip=0")

    total_free_ips = 0
    for ip_range in ip_range_envelope['documents'].values():
        start_ip = ip_to_int(ip_range['startIPAddress'])
        end_ip = ip_to_int(ip_range['endIPAddress'])
        total = end_ip - start_ip
        range_link = ip_range['documentSelfLink']
        free_ips = -1

        # Use external IP if configured
        if "ipamUser" and "ipamHost" and "ipamPassword" in inputs:
            ipam_url = "https://" + inputs["ipamHost"] + "/wapi/v2.10.5/" + quote(ip_range["id"]) + \
                    "?_return_fields%2b=utilization"
            ipam_auth = requests.auth.HTTPBasicAuth(username=inputs["ipamUser"],
                                                 password=context.getSecret(inputs["ipamPassword"]))
            if DEBUG:
                print("GET", ipam_url, end="")
                t = time.time()
            result = requests.get(ipam_url, auth=ipam_auth, verify=False)
            if DEBUG:
                print(" (%fs)" % (time.time() - t))
            if result.status_code != 200:
                # Handle this gracefully. We'll use cached data instead
                print("HTTP error %d: %s" % (result.status_code, result.content))
            else:
                ipam_record = result.json()
                print("Determined free IPs using live external IPAM data")
                free_ips = (1.0 - float(ipam_record["utilization"]) / 1000) * total

        # If we still don't have a value for free_ips, we either didn't have an external IPAM configured,
        # or the call to the IPAM failed. Fall back to the internal number in vRA. This could be unreliable.
        if free_ips == -1:
            if "customProperties" in ip_range and "freeIps" in ip_range["customProperties"]:
                # If we got a snapshot free IP count back from an external IPAM we use it,
                print("Determined free IPs using cached external IPAM data")
                free_ips = int(ip_range["customProperties"]["freeIps"])
            else:
                # Count the IPs that are used in this range based on vRA values. Might be
                # inaccurate for external IPAMs.
                ips = get(context,
                          "/provisioning/uerp/provisioning/mgmt/ip-address?expand&" +
                          mkfilter("((subnetRangeLink eq '%s') and (ipAddressStatus ne '*AVAILABLE*'))" % range_link) +
                          "&$orderby=name%20asc&$top=1&$skip=0")
                used = ips['totalCount']
                print("Determined free IPs using internal vRA data")
                free_ips = total - used
        total_free_ips += free_ips
        print("Range %s (subnet %s) has %d total and %d free" % (ip_range['name'], subnet, total, free_ips))
    cache[subnet] = total_free_ips
    print("*** Total free IPs for subnet %s is %d" % (ip_range["name"], total_free_ips))
    return total_free_ips


def get_blueprint(context, dep_id):
    dep = get(context, "/deployment/api/deployments/%s" % dep_id)

    # Deployments managed by [redacted] may have switched to an inline blueprint
    # after input changes. In that case, load the inline blueprint from a
    # hidden input.
    bp_id = dep["blueprintId"]
    if bp_id == "inline-blueprint":
        raw_bp = dep["inputs"]["__templateContent"].replace("\\$\\{", "${")
    else:
        raw_bp = get(context, "/blueprint/api/blueprints/%s" % bp_id)["content"]
    return yaml.safe_load(raw_bp)


def has_networks(bp, res_name):
    nics = bp["resources"][res_name]["properties"].get("networks", None)
    if nics is None:
        return False
    for nic in nics:
        if "network" in nic:
            return True
    return False


def get_network_types(bp, res_name):
    nics = bp["resources"][res_name]["properties"]["networks"]

    # Device index needs to be specified on all NICs or not at all. Everything else is an error.
    di_present = False
    for nic in nics:
        if "deviceIndex" in nic:
            di_present = True
        else:
            if di_present:
                raise Exception("deviceIndex must be present on all NICs or not at all")

    # If deviceIndex was present, we sort the list in that order
    if di_present:
        nics = sorted(nics, key=lambda nic: nic["deviceIndex"])

    nw_types = []
    for nic in nics:
        nw_node = nic.get("network", None)
        # If the network isn't explicitly declared, we assume it's an existing one
        if nw_node is None:
            nw_types.append("existing")
            continue
        m = re.match(r'\$\{\w+\.(\w+)', nw_node)
        if m is None:
            nw_types.append("existing")
            continue
        nw_key = m.group(1)
        nw_types.append(bp["resources"][nw_key]["properties"]["networkType"])
    return nw_types


def handler(context, inputs):
    outputs = inputs
    dep_id = inputs["deploymentId"]
    bp = get_blueprint(context, dep_id)

    # Preselect the network with the most available IPs
    selections = outputs['networkSelectionIds']
    component_id = inputs["componentId"].split("[")[0]
    for vm_idx in range(len(selections)):
        vm = selections[vm_idx]
        for nic_idx in range(len(vm)):
            nic = vm[nic_idx]
            print("Possible networks:" + json.dumps(nic))

            # Determine the network with the most available addresses
            best = reduce(lambda a, b:
                          a if get_available_ips(context, inputs, a) > get_available_ips(context, inputs, b) else b,
                          nic)

            # Create a new list with a single network, i.e. the one with the most IP addresses
            nic[:] = [best]
            free = get_available_ips(context, inputs, nic[0])
            print("Best subnet is %s with %d free IPs" % (nic[0], free))

        # vRA treats private networks strangely. They're not included in the inputs
        # but are expected in the outputs. We need to fill them out with dummy uuids.
        network_types = get_network_types(bp, component_id)
        adjusted_nics = []
        idx = 0
        for network_type in network_types:
            if network_type == "private":
                adjusted_nics.append(["00000000-0000-0000-0000-000000000000"])
            else:
                adjusted_nics.append(vm[idx])
                idx += 1
        vm[:] = adjusted_nics
    print("Resulting network selections: " + json.dumps(outputs['networkSelectionIds'], indent=4))
    return outputs
