[![Build Status](https://travis-ci.org/wtsi-hgi/openstack-info.svg?branch=master)](https://travis-ci.org/wtsi-hgi/openstack-info)
[![codecov](https://codecov.io/gh/wtsi-hgi/openstack-info/branch/master/graph/badge.svg)](https://codecov.io/gh/wtsi-hgi/openstack-info)


# OpenStack Info
_Gets information about what is in an OpenStack tenant._

## Installation
Prerequisites:
- python >= 3.6

Bleeding edge versions can be installed directly from GitHub:
```bash
git clone https://github.com/wtsi-hgi/openstack-info.git
cd openstack-tenant-cleaner
python setup.py install
```
or using pip:
```bash
pip install git+https://github.com/wtsi-hgi/openstack-info.git@master#egg=openstackinfo
```

## Usage
### CLI
Set environment variables:
```bash
export OS_USERNAME=user
export OS_TENANT_NAME=tenant
export OS_AUTH_URL=http://example.com:5000/v2.0/
export OS_PASSWORD=password
```

Then call:
```
openstackinfo
```
```json
TODO
```

Optionally set what the information is index by using `-i` or `--index`:
```bash
openstackinfo --index id
```
```json
TODO
```

### Python
```python
from openstackinfo.models import RunConfiguration, Credentials
from openstackinfo.helpers import get_information

configuration = RunConfiguration(credentials=Credentials(username, password, auth_url, tenant), indexer=INDEX_BY_ID)
openstack_info = get_information(configuration)
```


## Alternatives
- [shade](https://pypi.python.org/pypi/shade/) (underlying library: no CLI, no re-indexing).
- [Nova CLI](https://docs.openstack.org/python-novaclient/latest/cli/nova.html) (does not return JSON).
- [Openstack CLI](https://docs.openstack.org/python-openstackclient/latest/cli/) (does not return server metadata).
