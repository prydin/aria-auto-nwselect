# IPAM-Aware Network Selection for Aria Automation

## Motivation
This plugin allows for more optimized network selection when using the Infoblox IPAM. It uses the
_Network Configure_ event hook modify the list of selected networks, such that the network with
the most available IP addresses is always picked.

## Building from source

### Prerequisites
* Python 3.9+
* Pip 23.2+
* Maven 3.8+

### Steps
```commandline
cd <top of project directory>
mvn clean package
```

The ZIP package can be found in the `target` directory.

## Installation
1. In Aria Automation Assembler, go to Extensibility->Actions and click "Import action"
2. Add a subscription to "Network Configure" and attach the action "Network Select". 
Make sure the "Block Execution" checkbox is checked.
3. Add the following inputs to the action:
   1. ipamHost - IP address or hostname of the Infoblox host
   2. ipamUser - Name of Infoblox service account user
   3. ipamPassword - Encrypted action constant with Infoblox password.
