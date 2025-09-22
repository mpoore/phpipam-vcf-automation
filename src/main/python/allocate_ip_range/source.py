"""
Copyright (c) 2020 VMware, Inc.

This product is licensed to you under the Apache License, Version 2.0 (the "License").
You may not use this product except in compliance with the License.

This product may include a number of subcomponents with separate copyright notices
and license terms. Your use of these subcomponents is subject to the terms and
conditions of the subcomponent's license, as noted in the LICENSE file.

Modifications for phpIPAM by Michael Poore (@mpoore.io)
"""

import requests
from vra_ipam_utils.ipam import IPAM # type: ignore
import logging
import ipaddress

"""
Example payload

"inputs": {
    "resourceInfo": {
      "id": "/resources/sub-networks/255ac10c-0198-4a92-9414-b8e0c23c0204",
      "name": "net1-mcm223-126361015194",
      "type": "SUBNET",
      "orgId": "e0d6ea3a-519a-4308-afba-c973a8903250",
      "owner": "jason@csp.local",
      "properties": {
        "networkType": "PRIVATE",
        "datacenterId": "Datacenter:datacenter-21",
        "__networkCidr": "192.168.197.0/28",
        "__deploymentLink": "/resources/deployments/f77fbe4d-9e78-4b1b-93b0-024d342d0872",
        "__infrastructureUse": "true",
        "__composition_context_id": "f77fbe4d-9e78-4b1b-93b0-024d342d0872",
        "__isInfrastructureShareable": "true"
      }
    },
    "ipRangeAllocation": {
      "name": "net1-mcm223-126361015194",
      "ipBlockIds": [
        "block1",
        "block2"
      ],
      "properties": {
        "networkType": "PRIVATE",
        "datacenterId": "Datacenter:datacenter-21",
        "__networkCidr": "192.168.197.0/28",
        "__deploymentLink": "/resources/deployments/f77fbe4d-9e78-4b1b-93b0-024d342d0872",
        "__infrastructureUse": "true",
        "__composition_context_id": "f77fbe4d-9e78-4b1b-93b0-024d342d0872",
        "__isInfrastructureShareable": "true"
      },
      "subnetCidr": "192.168.197.0/28",
      "addressSpaceId": "default"
    },
    "endpoint": {
      "id": "f097759d8736675585c4c5d272cd",
      "endpointProperties": {
        "hostName": "sampleipam.sof-mbu.eng.vmware.com",
        "projectId": "111bb2f0-02fd-4983-94d2-8ac11768150f",
        "providerId": "d8a5e3f2-d839-4365-af5b-f48de588fdc1",
        "certificate": "-----BEGIN CERTIFICATE-----\nMIID0jCCArqgAwIBAgIQQaJF55UCb58f9KgQLD/QgTANBgkqhkiG9w0BAQUFADCB\niTELMAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExEjAQBgNVBAcTCVN1\nbm55dmFsZTERMA8GA1UEChMISW5mb2Jsb3gxFDASBgNVBAsTC0VuZ2luZWVyaW5n\nMSgwJgYDVQQDEx9pbmZvYmxveC5zb2YtbWJ1LmVuZy52bXdhcmUuY29tMB4XDTE5\nMDEyOTEzMDExMloXDTIwMDEyOTEzMDExMlowgYkxCzAJBgNVBAYTAlVTMRMwEQYD\nVQQIEwpDYWxpZm9ybmlhMRIwEAYDVQQHEwlTdW5ueXZhbGUxETAPBgNVBAoTCElu\nZm9ibG94MRQwEgYDVQQLEwtFbmdpbmVlcmluZzEoMCYGA1UEAxMfaW5mb2Jsb3gu\nc29mLW1idS5lbmcudm13YXJlLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCC\nAQoCggEBAMMLNTqbAri6rt/H8iC4UgRdN0qj+wk0R2blmD9h1BiZJTeQk1r9i2rz\nzUOZHvE8Bld8m8xJ+nysWHaoFFGTX8bOd/p20oJBGbCLqXtoLMMBGAlP7nzWGBXH\nBYUS7kMv/CG+PSX0uuB0pRbhwOFq8Y69m4HRnn2X0WJGuu+v0FmRK/1m/kCacHga\nMBKaIgbwN72rW1t/MK0ijogmLR1ASY4FlMn7OBHIEUzO+dWFBh+gPDjoBECTTH8W\n5AK9TnYdxwAtJRYWmnVqtLoT3bImtSfI4YLUtpr9r13Kv5FkYVbXov1KBrQPbYyp\n72uT2ZgDJT4YUuWyKpMppgw1VcG3MosCAwEAAaM0MDIwMAYDVR0RBCkwJ4cEChda\nCoIfaW5mb2Jsb3guc29mLW1idS5lbmcudm13YXJlLmNvbTANBgkqhkiG9w0BAQUF\nAAOCAQEAXFPIh00VI55Sdfx+czbBb4rJz3c1xgN7pbV46K0nGI8S6ufAQPgLvZJ6\ng2T/mpo0FTuWCz1IE9PC28276vwv+xJZQwQyoUq4lhT6At84NWN+ZdLEe+aBAq+Y\nxUcIWzcKv8WdnlS5DRQxnw6pQCBdisnaFoEIzngQV8oYeIemW4Hcmb//yeykbZKJ\n0GTtK5Pud+kCkYmMHpmhH21q+3aRIcdzOYIoXhdzmIKG0Och97HthqpvRfOeWQ/A\nPDbxqQ2R/3D0gt9jWPCG7c0lB8Ynl24jLBB0RhY6mBrYpFbtXBQSEciUDRJVB2zL\nV8nJiMdhj+Q+ZmtSwhNRvi2qvWAUJQ==\n-----END CERTIFICATE-----\n"
      },
      "authCredentialsLink": "/core/auth/credentials/13c9cbade08950755898c4b89c4a0"
    }
  }
"""
def handler(context, inputs):

    ipam = IPAM(context, inputs)
    IPAM.do_allocate_ip_range = do_allocate_ip_range

    return ipam.allocate_ip_range()

def do_allocate_ip_range(self, auth_credentials, cert):
    # Prepare endpoint
    appId = auth_credentials["privateKeyId"]
    appCode = auth_credentials["privateKey"]
    hostname = self.inputs["endpoint"]["endpointProperties"]["hostName"]
    token = {
        "phpipam-token": appCode
    }
    baseUri = f'https://{hostname}/api/{appId}'
    logging.info(f"endpoint configuration complete for {baseUri}")

    resource = self.inputs["resourceInfo"]
    allocation = self.inputs["ipRangeAllocation"]
    ipRange = allocate(resource, allocation, self.context, self.inputs["endpoint"], baseUri, token, cert)

    return {
        "ipRange": ipRange
    }

def allocate(resource, allocation, context, endpoint, baseUri, token, cert):

    lastError = None
    for ipBlockId in allocation["ipBlockIds"]:

        logging.info(f"attempting to allocate from subnet {ipBlockId}")
        try:
            return allocate_in_ip_block(ipBlockId, resource, allocation, context, endpoint, baseUri, token, cert)
        except Exception as e:
            lastError = e
            logging.error(f"failed to allocate from subnet {ipBlockId}: {str(e)}")

    logging.error("no more subnets, raising last error")
    raise lastError

def allocate_in_ip_block(ipBlockId, resource, allocation, context, endpoint, baseUri, token, cert):
    # Get subnet prefix length
    prefixLength = allocation['subnetPrefixLength']

    # Request new subnet from block
    subnetUri = f'{baseUri}/subnets/{ipBlockId}/first_subnet/{prefixLength}/'
    subnetReq = requests.post(subnetUri, headers=token, verify=cert)
    subnetRes = subnetReq.json()

    # Process result
    if subnetRes['success']:
        logging.info(f"successfully created subnet {subnetRes['id']} from subnet {ipBlockId}")
        subnetId = subnetRes['id']
    else:
        raise Exception(f"a new subnet could not be created: {subnetRes['message']}")
    
    # Configure nameservers etc. to match parent subnet
    # Get parent subnet
    subnetUri = f'{baseUri}/subnets/{ipBlockId}/'
    subnetReq = requests.get(subnetUri, headers=token, verify=cert)
    subnetRes = subnetReq.json()
    if subnetRes['success']:
        logging.info(f"successfully retrieved subnet {ipBlockId}")
        subnetRes = subnetReq.json()['data']
    else:
        raise Exception(f"could not retrieve subnet {ipBlockId}: {subnetRes['message']}")
    
    # Prepare subnet update
    requestData = {}
    dnsDomainField = endpoint["endpointProperties"]["dnsDomain"]
    dnsSearchDomainsField = endpoint["endpointProperties"]["dnsSearchDomains"]
    if str(subnetRes['nameserverId']) != "0":
       requestData['nameserverId'] = subnetRes['nameserverId']
    if dnsDomainField != "":
      try:
        requestData[f'custom_{dnsDomainField}'] = subnetRes[f'custom_{dnsDomainField}']
      except:
        logging.warning(f"could not obtain the DNS domain for the subnet {ipBlockId}")
    if dnsSearchDomainsField != "":
      try:
        requestData[f'custom_{dnsSearchDomainsField}'] = subnetRes[f'custom_{dnsSearchDomainsField}']
      except:
        logging.warning(f"could not obtain the DNS search domains for the subnet {ipBlockId}")
    requestData['id'] = subnetId
    logging.info(f"updating subnet {subnetId} with requestData: {requestData}")

    # Execute subnet update
    subnetUri = f'{baseUri}/subnets/'
    subnetReq = requests.patch(subnetUri, requestData, headers=token, verify=cert)
    subnetRes = subnetReq.json()

    # Process result
    if subnetRes['success']:
        logging.info(f"successfully updated subnet {subnetId}")
    else:
        raise Exception(f"the subnet could not be updated: {subnetRes['message']}")

    # Get subnet details
    logging.info(f"returning details for subnet {subnetId}")
    result = {}
    subnetUri = f'{baseUri}/subnets/{subnetId}/'
    subnetReq = requests.get(subnetUri, headers=token, verify=cert)
    subnetRes = subnetReq.json()['data']

    # Process result
    result['id'] = str(subnetRes['id'])
    result['name'] = f"{str(subnetRes['subnet'])}/{str(subnetRes['mask'])}"
    result['description'] = str(subnetRes['description'])
    subnetInfo = ipaddress.ip_network(str(subnetRes['subnet']) + '/' + str(subnetRes['mask']))
    result['ipVersion'] = 'IPv' + str(subnetInfo.version)
    result['startIPAddress'] = str(subnetInfo[1])
    result['endIPAddress'] = str(subnetInfo[-2])
    result['gatewayAddress'] = str(subnetInfo[-2])
    result['subnetPrefixLength'] = str(subnetRes['mask'])
    result['addressSpaceId'] = 'default'
    # Nameserver details
    try:
      result['dnsServerAddresses'] = [server.strip() for server in str(subnetRes['nameservers']['namesrv1']).split(';')]
    except:
      result['dnsServerAddresses'] = []
      logging.warning(f"could not obtain the DNS servers for subnet {subnetId}")
    # DNS domain and search details
    dnsDomainField = endpoint["endpointProperties"]["dnsDomain"]
    dnsSearchDomainsField = endpoint["endpointProperties"]["dnsSearchDomains"]
    if dnsDomainField != "":
      try:
        result['domain'] = str(subnetRes[f'custom_{dnsDomainField}'])
      except:
        result['domain'] = ""
        logging.warning(f"could not obtain the DNS domain for subnet {subnetId}")
    if dnsSearchDomainsField != "":
      try:
        result['dnsSearchDomains'] = [domain.strip() for domain in str(subnetRes[f'custom_{dnsSearchDomainsField}']).split(',')]
      except:
        result['dnsSearchDomains'] = []
        logging.warning(f"could not obtain the DNS search domains for subnet {subnetId}")

    return result