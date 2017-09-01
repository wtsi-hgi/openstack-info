import jsonschema
from typing import Dict, Any

ID_JSON_KEY = "id"
TYPE_JSON_KEY = "type"

OPENSTACK_INSTANCES_JSON_KEY = "instances"
OPENSTACK_VOLUMES_JSON_KEY = "volumes"
OPENSTACK_NETWORKS_JSON_KEY = "networks"
OPENSTACK_SECURITY_GROUPS_JSON_KEY = "security_groups"

RESOURCE_TYPE_MAPPINGS = {
    OPENSTACK_SECURITY_GROUPS_JSON_KEY: "security_group",
    OPENSTACK_INSTANCES_JSON_KEY: "instance",
    OPENSTACK_NETWORKS_JSON_KEY: "network",
    OPENSTACK_VOLUMES_JSON_KEY: "volume"
}

INDEX_BY_TYPE_SCHEMA = {
    "type": "object",
    "properties": {
        OPENSTACK_INSTANCES_JSON_KEY: {
            "type": "object"
        },
        OPENSTACK_VOLUMES_JSON_KEY: {
            "type": "object"
        },
        OPENSTACK_NETWORKS_JSON_KEY: {
            "type": "object"
        },
        OPENSTACK_SECURITY_GROUPS_JSON_KEY: {
            "type": "object"
        }
    }
}


class ValidationError(ValueError):
    """
    Raised if the validation against a schema fails.
    """


def validate(instance: Any, schema: Dict):
    """
    Validates the given instance against a JSON schema.
    :param instance: to be validated
    :param schema: to validate against
    :raises ValidationError: if instance does not validate against the schema
    """
    try:
        jsonschema.validate(instance, schema)
    except jsonschema.exceptions.ValidationError as e:
        raise ValidationError(e.message) from e
