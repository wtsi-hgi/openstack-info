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
{
    "instances": [
        {
            "created": "2017-06-12T14:13:45Z",
            "id": "f875eb56-760f-49b4-950d-7c97c4418cf5",
            "metadata": {
                "hello": "world"
            },
            "name": "some-server",
            "networks": [],
            "security_groups": [
                "2a258c8f-f4c9-45e6-bcba-48cead5e5fcd"
            ],
            "status": "ACTIVE",
            "updated": "2017-06-12T14:14:35Z",
            "volumes_attached": [
                "9b88ef64-d686-4ae4-9db8-c649adbe2ac9"
            ]
        }
    ],
    "networks": [
        {
            "id": "97365eaf-1d88-4d20-81a0-2ece5de5525c",
            "name": "hgi",
            "subnet_ids": [
                "ec0aa86b-b89b-40bd-b2c9-540e82ec54c9"
            ]
        }
    ],
    "security_groups": [
        {
            "id": "2a258c8f-f4c9-45e6-bcba-48cead5e5fcd",
            "name": "ssh"
        }
    ],
    "volumes": [
        {
            "attached_to": [
                "f875eb56-760f-49b4-950d-7c97c4418cf5"
            ],
            "id": "9b88ef64-d686-4ae4-9db8-c649adbe2ac9",
            "name": "data"
        }
    ]
}
```

Optionally set what the information is index by using `-i` or `--index`:
```bash
openstackinfo --index id
```
```json
{
    "2a258c8f-f4c9-45e6-bcba-48cead5e5fcd": {
        "id": "2a258c8f-f4c9-45e6-bcba-48cead5e5fcd",
        "name": "ssh",
        "type": "security_group"
    },
    "97365eaf-1d88-4d20-81a0-2ece5de5525c": {
        "id": "97365eaf-1d88-4d20-81a0-2ece5de5525c",
        "name": "hgi",
        "subnet_ids": [
            "ec0aa86b-b89b-40bd-b2c9-540e82ec54c9"
        ],
        "type": "network"
    },
    "9b88ef64-d686-4ae4-9db8-c649adbe2ac9": {
        "attached_to": [
            "f875eb56-760f-49b4-950d-7c97c4418cf5"
        ],
        "id": "9b88ef64-d686-4ae4-9db8-c649adbe2ac9",
        "name": "data",
        "type": "volume"
    },
    "f875eb56-760f-49b4-950d-7c97c4418cf5": {
        "created": "2017-06-12T14:13:45Z",
        "id": "f875eb56-760f-49b4-950d-7c97c4418cf5",
        "metadata": {
            "hello": "world"
        },
        "name": "some-server",
        "networks": [],
        "security_groups": [
            "2a258c8f-f4c9-45e6-bcba-48cead5e5fcd"
        ],
        "status": "ACTIVE",
        "type": "instance",
        "updated": "2017-06-12T14:14:35Z",
        "volumes_attached": [
            "9b88ef64-d686-4ae4-9db8-c649adbe2ac9"
        ]
    }
}
```

### Python
```python
from openstackinfo import get_openstack_info, Credentials

openstack_info = get_openstack_info(Credentials(username, password, auth_url, tenant))
```


## Alternatives
- [Nova CLI](https://docs.openstack.org/python-novaclient/latest/cli/nova.html) (does not return JSON).
- [Openstack CLI](https://docs.openstack.org/python-openstackclient/latest/cli/) (does not return server metadata).
