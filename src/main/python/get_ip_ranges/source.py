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

'''
Example payload:

"inputs": {
    "endpoint": {
      "id": "f097759d8736675585c4c5d272cd",
      "authCredentialsLink": "/core/auth/credentials/13c9cbade08950755898c4b89c4a0",
      "endpointProperties": {
        "hostName": "sampleipam.sof-mbu.eng.vmware.com",
        "certificate": "-----BEGIN CERTIFICATE-----\nMIID0jCCArqgAwIBAgIQQaJF55UCb58f9KgQLD/QgTANBgkqhkiG9w0BAQUFADCB\niTELMAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExEjAQBgNVBAcTCVN1\nbm55dmFsZTERMA8GA1UEChMISW5mb2Jsb3gxFDASBgNVBAsTC0VuZ2luZWVyaW5n\nMSgwJgYDVQQDEx9pbmZvYmxveC5zb2YtbWJ1LmVuZy52bXdhcmUuY29tMB4XDTE5\nMDEyOTEzMDExMloXDTIwMDEyOTEzMDExMlowgYkxCzAJBgNVBAYTAlVTMRMwEQYD\nVQQIEwpDYWxpZm9ybmlhMRIwEAYDVQQHEwlTdW5ueXZhbGUxETAPBgNVBAoTCElu\nZm9ibG94MRQwEgYDVQQLEwtFbmdpbmVlcmluZzEoMCYGA1UEAxMfaW5mb2Jsb3gu\nc29mLW1idS5lbmcudm13YXJlLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCC\nAQoCggEBAMMLNTqbAri6rt/H8iC4UgRdN0qj+wk0R2blmD9h1BiZJTeQk1r9i2rz\nzUOZHvE8Bld8m8xJ+nysWHaoFFGTX8bOd/p20oJBGbCLqXtoLMMBGAlP7nzWGBXH\nBYUS7kMv/CG+PSX0uuB0pRbhwOFq8Y69m4HRnn2X0WJGuu+v0FmRK/1m/kCacHga\nMBKaIgbwN72rW1t/MK0ijogmLR1ASY4FlMn7OBHIEUzO+dWFBh+gPDjoBECTTH8W\n5AK9TnYdxwAtJRYWmnVqtLoT3bImtSfI4YLUtpr9r13Kv5FkYVbXov1KBrQPbYyp\n72uT2ZgDJT4YUuWyKpMppgw1VcG3MosCAwEAAaM0MDIwMAYDVR0RBCkwJ4cEChda\nCoIfaW5mb2Jsb3guc29mLW1idS5lbmcudm13YXJlLmNvbTANBgkqhkiG9w0BAQUF\nAAOCAQEAXFPIh00VI55Sdfx+czbBb4rJz3c1xgN7pbV46K0nGI8S6ufAQPgLvZJ6\ng2T/mpo0FTuWCz1IE9PC28276vwv+xJZQwQyoUq4lhT6At84NWN+ZdLEe+aBAq+Y\nxUcIWzcKv8WdnlS5DRQxnw6pQCBdisnaFoEIzngQV8oYeIemW4Hcmb//yeykbZKJ\n0GTtK5Pud+kCkYmMHpmhH21q+3aRIcdzOYIoXhdzmIKG0Och97HthqpvRfOeWQ/A\nPDbxqQ2R/3D0gt9jWPCG7c0lB8Ynl24jLBB0RhY6mBrYpFbtXBQSEciUDRJVB2zL\nV8nJiMdhj+Q+ZmtSwhNRvi2qvWAUJQ==\n-----END CERTIFICATE-----\n"
      }
    },
    "pagingAndSorting": {
      "maxResults": 1000,
      "pageToken": "789c55905d6e02310c84df7d91452a456481168ec04b55950344f9db55dadd384abc056e5f3b42adfa12299f279ec9ac7c5670e9b0045a4ad2430c93af7a465f3bc83d4f9e3aa8976e6681ce660c827770de2aa1a68c72dfc3cae74393999b2e4df302e72691373aa60199bd827398efac18810f87a952591c61817c849513999df0b6c11436d6d400effcfacc14f2099cd6768913c5a435a0fd0c8e20ab2dbcd147564a2228c93b60b99ae2d94efde6ac640a09d9331130c539367078c41c915067ac9122268dc350439bf3379e9bc01b32025e9bd111aa65c829e89e83f0135ba740572c5f525c73f95faa608e39e55e62c6fcbd37de9775b891212a758d59bceb7a0eb30d7c7f6cd35c1399984291053b30f29fc5feed6cedf7adfe21962ab17b8ebde5089b1fec0d97d7-e5c4e5a1d726f600c22ebfd9f186148a1449755fd79a69ceabfe2aa"
    }
  }
'''
def handler(context, inputs):

    ipam = IPAM(context, inputs)
    IPAM.do_get_ip_ranges = do_get_ip_ranges

    return ipam.get_ip_ranges()

def do_get_ip_ranges(self, auth_credentials, cert):
    # Prepare endpoint
    appId = auth_credentials["privateKeyId"]
    appCode = auth_credentials["privateKey"]
    hostname = self.inputs["endpoint"]["endpointProperties"]["hostName"]
    token = {
        "phpipam-token": appCode
    }
    baseUri = f'https://{hostname}/api/{appId}'
    logging.info(f"endpoint configuration complete for {baseUri}")

    # Configure filter behaviour
    enableFilter = self.inputs["endpoint"]["endpointProperties"]["enableFilter"]
    filterField = self.inputs["endpoint"]["endpointProperties"]["filterField"]
    filterValue = self.inputs["endpoint"]["endpointProperties"]["filterValue"]
    filterMatch = self.inputs["endpoint"]["endpointProperties"]["filterMatch"]
    if enableFilter == "true":
      if filterMatch == "":
        queryFilter = f'filter_by={filterField}&filter_value={filterValue}'
      else:
        queryFilter = f'filter_by={filterField}&filter_value={filterValue}&filter_match={filterMatch}'
      logging.info(f"subnet filter: {queryFilter}")
    else:
      queryFilter = ""

    # Configure query pagination - Not supported by phpIPAM

    # Query subnets
    ipRanges = []
    subnetUri = f'{baseUri}/subnets/'
    allSubnetsReq = requests.get(f'{subnetUri}?{queryFilter}', headers=token, verify=cert)
    allSubnetsRes = allSubnetsReq.json()['data']
    logging.info(f"query returned {len(allSubnetsRes)} results")

    # Parse results
    for subnet in allSubnetsRes:
      if str(subnet['allowRequests']) == "1":
        # Basic information
        ipRange = {}
        ipRange['id'] = str(subnet['id'])
        ipRange['name'] = f"{str(subnet['subnet'])}/{str(subnet['mask'])}"
        ipRange['description'] = str(subnet['description'])
        logging.info(f"discovered range {ipRange['id']}, with name: {ipRange['name']}, and description: {ipRange['description']}")

        # Range details
        rangeInfo = ipaddress.ip_network(str(subnet['subnet']) + '/' + str(subnet['mask']))
        ipRange['ipVersion'] = 'IPv' + str(rangeInfo.version)
        ipRange['startIPAddress'] = str(rangeInfo[1])
        ipRange['endIPAddress'] = str(rangeInfo[-2])
        ipRange['subnetPrefixLength'] = str(subnet['mask'])
        ipRange['addressSpaceId'] = 'default'

        # Nameserver details
        try:
          ipRange['dnsServerAddresses'] = [server.strip() for server in str(subnet['nameservers']['namesrv1']).split(';')]
        except:
          ipRange['dnsServerAddresses'] = []
          logging.warning(f"could not obtain the DNS servers for the range with ID: {ipRange['id']}")

        # DNS domain and search details
        dnsDomainField = self.inputs["endpoint"]["endpointProperties"]["dnsDomain"]
        dnsSearchDomainsField = self.inputs["endpoint"]["endpointProperties"]["dnsSearchDomains"]
        if dnsDomainField != "":
          try:
            ipRange['domain'] = str(subnet[f'custom_{dnsDomainField}'])
          except:
            ipRange['domain'] = ""
            logging.warning(f"could not obtain the DNS domain for the range with ID: {ipRange['id']}")
        if dnsSearchDomainsField != "":
          try:
            ipRange['dnsSearchDomains'] = [domain.strip() for domain in str(subnet[f'custom_{dnsSearchDomainsField}']).split(',')]
          except:
            ipRange['dnsSearchDomains'] = []
            logging.warning(f"could not obtain the DNS search domains for the range with ID: {ipRange['id']}")

        # Gateway details
        subnetGatewayReq = requests.get(f"{subnetUri}/{subnet['id']}/addresses/?filter_by=is_gateway&filter_value=1", headers=token, verify=cert)
        if subnetGatewayReq.status_code == 200 and 'data' in subnetGatewayReq.json():
          ipRange['gatewayAddress'] = subnetGatewayReq.json()['data'][0]['ip']
        else:
          logging.info(f"the range with ID: {ipRange['id']} does not have a default gateway defined")
        
        # Add range to results
        ipRanges.append(ipRange)

    # Return results
    result = {
        "ipRanges" : ipRanges
    }
    return result