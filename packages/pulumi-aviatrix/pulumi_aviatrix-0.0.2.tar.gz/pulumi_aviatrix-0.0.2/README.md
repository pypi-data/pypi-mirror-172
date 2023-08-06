# Aviatrix Resource Provider

The Aviatrix Resource Provider lets you manage [Aviatrix](https://aviatrix.com) resources.

## Installing

This package is currently available for the following platforms/languages:

### Python

To use from Python, install using `pip`:

```bash
pip install pulumi-aviatrix
```

## Configuration

The following configuration points are available for the `aviatrix` provider:

Mandatory:
- `aviatrix:controllerIp` (environment: `AVIATRIX_CONTROLLERIP`) - The Aviatrix controller's IP address
- `aviatrix:username` (environment: `AVIATRIX_USERNAME`) - The Aviatrix controller's username
- `aviatrix:password` (environment: `AVIATRIX_PASSWORD`) - The Aviatrix controller's password

Optional:
- `aviatrix:skip_version_validation` (environment: `AVIATRIX_SKIP_VERSION_VALIDATION`) - Valid values: true, false. Default: false. If set to true, it skips checking whether current Pulumi provider supports current Controller version.
- `aviatrix:verify_ssl_certificate` (environment: `AVIATRIX_VERIFY_SSL_CERTIFICATE`) - Valid values: true, false. Default: false. If set to true, the SSL certificate of the controller will be verified.

## Reference

For detailed reference documentation, please visit [the Terraform registry](https://registry.terraform.io/providers/AviatrixSystems/aviatrix/latest/docs).

## Disclaimer
The material embodied in this software/code is provided to you "as-is" and without warranty of any kind, express, implied or otherwise, including without limitation, any warranty of fitness for a particular purpose. In no event shall the Aviatrix Inc. be liable to you or anyone else for any direct, special, incidental, indirect or consequential damages of any kind, or any damages whatsoever, including without limitation, loss of profit, loss of use, savings or revenue, or the claims of third parties, whether or not Aviatrix Inc. has been advised of the possibility of such loss, however caused and on any theory of liability, arising out of or in connection with the possession, use or performance of this software/code.
