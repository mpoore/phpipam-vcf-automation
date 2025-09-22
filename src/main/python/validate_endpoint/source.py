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
from vra_ipam_utils.exceptions import InvalidCertificateException # type: ignore
import logging

'''
Example payload:

"inputs": {
    "authCredentialsLink": "/core/auth/credentials/13c9cbade08950755898c4b89c4a0",
    "endpointProperties": {
      "hostName": "sampleipam.sof-mbu.eng.vmware.com"
    }
  }
'''

def handler(context, inputs):

    ipam = IPAM(context, inputs)
    IPAM.do_validate_endpoint = do_validate_endpoint

    return ipam.validate_endpoint()

def do_validate_endpoint(self, auth_credentials, cert):
    # Prepare endpoint
    appId = auth_credentials["privateKeyId"]
    appCode = auth_credentials["privateKey"]
    hostname = self.inputs["endpointProperties"]["hostName"]
    token = {
        "phpipam-token": appCode
    }
    baseUri = f'https://{hostname}/api/{appId}/user/'
    logging.info(f"endpoint configuration complete for {baseUri}")

    try:
        response = requests.get(baseUri, verify=cert, headers=token)

        if response.status_code == 200:
            logging.info("endpoint connected successfully")
            return {
                "message": "Validated successfully",
                "statusCode": "200"
            }
        elif response.status_code == 500 and response.json()['message'] == 'Invalid appId or appCode':
            logging.error(f"invalid credentials error: {str(response.content)}")
            raise Exception(f"invalid credentials error: {str(response.content)}")
        else:
            raise Exception(f"failed to connect: {str(response.content)}")
    except Exception as e:
        """ In case of SSL validation error, a InvalidCertificateException is raised.
            So that the IPAM SDK can go ahead and fetch the server certificate
            and display it to the user for manual acceptance.
        """
        if "SSLCertVerificationError" in str(e) or "CERTIFICATE_VERIFY_FAILED" in str(e) or 'certificate verify failed' in str(e):
            raise InvalidCertificateException("certificate verify failed", self.inputs["endpointProperties"]["hostName"], 443) from e

        raise e