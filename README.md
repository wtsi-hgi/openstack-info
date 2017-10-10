[![Build Status](https://travis-ci.org/wtsi-hgi/openstack-info.svg?branch=master)](https://travis-ci.org/wtsi-hgi/openstack-info)
[![codecov](https://codecov.io/gh/wtsi-hgi/openstack-info/branch/master/graph/badge.svg)](https://codecov.io/gh/wtsi-hgi/openstack-info)

# OpenStack Info
_Gets information about what is in an OpenStack tenant._


## Installation
Prerequisites:
- python >= 3.6

The tool can be installed from PyPi:
```bash
pip install openstackinfo
```

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
```bash
openstackinfo
```

The available options can be found with `openstackinfo -h`:
```
usage: openstackinfo [-h] [-i {type,id}] [--max-connections MAX_CONNECTIONS]
                     [--retries RETRIES] [--retry-wait RETRY_WAIT]
                     [--retry-wait-multiplier RETRY_WAIT_MULTIPLIER]

Openstack tenant information retriever

optional arguments:
  -h, --help            show this help message and exit
  -i {type,id}, --index {type,id}
                        What the OpenStack information should be index by
                        (default: type)
  --max-connections MAX_CONNECTIONS
                        Maximum number of simultaneous connections to make to
                        OpenStack. Configured automatically if not set
                        (default: None)
  --retries RETRIES     Number of times to retry getting information about a
                        particular tpye of OpenStack resource (default: 3)
  --retry-wait RETRY_WAIT
                        Initial amount of time (in seconds) to wait after a
                        failure before retrying (default: 1.0)
  --retry-wait-multiplier RETRY_WAIT_MULTIPLIER
                        Multiplier that is applied to the wait time after each
                        failure. e.g. An initial wait time of 1.0s, a wait
                        multiplier of 5.0, and a maximum of 3 retries will
                        result in the waits between retries of [1.0s, 5.0s,
                        25.0s] (default: 5.0)
  --retry-wait-deviation RETRY_WAIT_DEVIATION
                        To minimise collisions, the wait time before retrying
                        a request is randomised to plus or minus the value of
                        this parameter as a percentage of the total wait time.
                        e.g. A wait time of 1.0s and max deviation percentage
                        of 10.0 will result in an actual wait between 0.9s and
                        1.1s (default: 10.0)
```

### Python
```python
from openstackinfo.retriever.models import Credentials
from openstackinfo.retriever.retrievers import ShadeInformationRetriever
from openstackinfo.helpers import get_information, RunConfiguration
from openstackinfo.indexers import InformationIndexerByType

retriever = ShadeInformationRetriever(credentials=Credentials(username, password, auth_url, tenant))
configuration = RunConfiguration(retriever=retriever, indexer=InformationIndexerByType)
openstack_info = get_information(configuration)
```


## Alternatives
- [shade](https://pypi.python.org/pypi/shade/) (underlying library: no CLI, no re-indexing).
- [Nova CLI](https://docs.openstack.org/python-novaclient/latest/cli/nova.html) (does not return JSON).
- [Openstack CLI](https://docs.openstack.org/python-openstackclient/latest/cli/) (does not return server metadata).
