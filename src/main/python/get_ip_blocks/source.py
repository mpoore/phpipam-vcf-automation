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
      "pageToken": "87811419dec2112cda2aa29685685d650ac1f61f"
    }
  }
'''
def handler(context, inputs):

    ipam = IPAM(context, inputs)
    IPAM.do_get_ip_blocks = do_get_ip_blocks

    return ipam.get_ip_blocks()

def do_get_ip_blocks(self, auth_credentials, cert):
    # Configure IP block functionality
    enableIPBlocks = self.inputs["endpoint"]["endpointProperties"]["enableIPBlocks"]
    isBlockField = self.inputs["endpoint"]["endpointProperties"]["isBlockField"]
    if enableIPBlocks != "true":
      logging.info("IP blocks functionality is disabled in endpoint configuration")
      result = {
        "ipBlocks" : []
      }
      return result

    # Prepare endpoint
    appId = auth_credentials["privateKeyId"]
    appCode = auth_credentials["privateKey"]
    hostname = self.inputs["endpoint"]["endpointProperties"]["hostName"]
    token = {
        "phpipam-token": appCode
    }
    baseUri = f'https://{hostname}/api/{appId}'
    logging.info(f"endpoint configuration prepared for {baseUri}")

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
    ipBlocks = []
    subnetUri = f'{baseUri}/subnets/'
    allSubnetsReq = requests.get(f'{subnetUri}?{queryFilter}', headers=token, verify=cert)
    allSubnetsRes = allSubnetsReq.json()['data']
    logging.info(f"query returned {len(allSubnetsRes)} results")

    # Parse results
    for subnet in allSubnetsRes:
      if str(subnet[f"custom_{isBlockField}"]) == "1":
        # Basic information
        ipBlock = {}
        ipBlock['id'] = str(subnet['id'])
        ipBlock['name'] = f"{str(subnet['subnet'])}/{str(subnet['mask'])}"
        ipBlock['ipBlockCIDR'] = f"{str(subnet['subnet'])}/{str(subnet['mask'])}"
        ipBlock['description'] = str(subnet['description'])
        logging.info(f"discovered block with ID: {ipBlock['id']}, Name: {ipBlock['name']}, and Description: {ipBlock['description']}")

        # Range details
        rangeInfo = ipaddress.ip_network(str(subnet['subnet']) + '/' + str(subnet['mask']))
        ipBlock['ipVersion'] = 'IPv' + str(rangeInfo.version)
        ipBlock['addressSpaceId'] = 'default'

        # Nameserver details
        try:
          ipBlock['dnsServerAddresses'] = [server.strip() for server in str(subnet['nameservers']['namesrv1']).split(';')]
        except:
          ipBlock['dnsServerAddresses'] = []
          logging.warning(f"could not obtain the DNS servers for the block with ID: {ipBlock['id']}")

        # DNS domain and search details
        dnsDomainField = self.inputs["endpoint"]["endpointProperties"]["dnsDomain"]
        dnsSearchDomainsField = self.inputs["endpoint"]["endpointProperties"]["dnsSearchDomains"]
        if dnsDomainField != "":
          try:
            ipBlock['domain'] = str(subnet[f'custom_{dnsDomainField}'])
          except:
            ipBlock['domain'] = ""
            logging.warning(f"could not obtain the DNS domain for the block with ID: {ipBlock['id']}")
        if dnsSearchDomainsField != "":
          try:
            ipBlock['dnsSearchDomains'] = [domain.strip() for domain in str(subnet[f'custom_{dnsSearchDomainsField}']).split(',')]
          except:
            ipBlock['dnsSearchDomains'] = []
            logging.warning(f"could not obtain the DNS search domains for the block with ID: {ipBlock['id']}")
        
        # Add range to results
        ipBlocks.append(ipBlock)

    # Return results
    result = {
        "ipBlocks" : ipBlocks
    }
    return result