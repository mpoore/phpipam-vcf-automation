# phpIPAM integration for VMware VCF Automation 8.x

This integration allows VMware VCF Automation 8.x to use [phpIPAM](https://phpipam.net) for assigning static IP addresses to provisioned virtual machines and on-demand networks.

## About VMware VCF Automation

VMware VCF Automation (formerly known as VMware Aria Automation and vRealize Automation) is VMware’s enterprise-grade platform for automating the deployment, configuration, and lifecycle management of cloud and on-premises infrastructure. It enables organizations to deliver infrastructure and application services consistently and at scale, leveraging policy-based governance and self-service capabilities.

A feature of VCF Automation is its integration with IP Address Management (IPAM) solutions, such as phpIPAM or Infoblox, allowing automated allocation, tracking, and management of IP addresses during the provisioning of virtual networks and workloads. This ensures IP consistency, avoids conflicts, and streamlines network automation workflows within VMware Cloud Foundation (VCF) environments.

## About phpIPAM

[phpIPAM](https://phpipam.net/) is an open-source IP address management (IPAM) solution designed to help organizations efficiently manage and track their IPv4 and IPv6 address space. Built with PHP, MySQL, and jQuery, it provides a modern and user-friendly web interface for managing subnets, IP addresses, VLANs, VRFs, and related network resources.

phpIPAM is lightweight, easy to deploy, and integrates well with network automation workflows, making it ideal for both small labs and large-scale enterprise environments.

- [phpIPAM documentation](https://phpipam.net/documents/all-documents/)
- [phpIPAM REST API documentation](https://phpipam.net/api/api_documentation/)

## Documentation
Documentation for this integration and its use in conjunction with VCF Automation and phpIPAM is available in the docs folder. The documentation is not intended to provide detailed guidance for either VCF Automation or phpIPAM beyond the scope of this integration.

The following documentation pages are available:
- [Installation](docs/install.md) - How to download and install this integration.
- [Prerequisites](docs/prerequisites.md) - Preparing phpIPAM to use this integration.
- [Basic Configuration](docs/configure-basic.md) - Creating a basic connection for VCF Automation to phpIPAM using this integration.
- [Filter Configuration](docs/configure-filter.md) - Using the filtering functionality to target specific subnets in phpIPAM.
- [DNS Configuration](docs/configure-dns.md) - Populating DNS related fields in VCF Automation using fields in phpIPAM.
- [On-Demand Networks](docs/configure-ondemand.md) - Using VCF Automation's on-demand networks capabilities with NSX and phpIPAM.
- [Troubleshooting](docs/troubleshooting.md) - Some common problem areas and how to investigate them.

## Feedback and Issues

Whilst reasonable efforts have been made to test this integration, problems may still occur. The integration's author offers no warranty for its use. That said, if you do encounter a bug or have an idea for a change or improvement, please feel free to open an [Issue](https://github.com/mpoore/phpipam-vcf-automation/issues) on this repository.

Please include as much information as possible in any created issues, for example:
- The version of phpIPAM used
- The version of VCF Automation used
- The version of this integration used
- Details of the problem being seen
- Any relevant log messages from the action runs in VCF Automation (see the [Troubleshooting](docs/troubleshooting.md) documentation page for how to view these)