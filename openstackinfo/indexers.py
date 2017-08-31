import json

from typing import Dict

from openstackinfo.serialisation import OPENSTACK_SECURITY_GROUPS_JSON_KEY, OPENSTACK_INSTANCES_JSON_KEY, \
    OPENSTACK_NETWORKS_JSON_KEY, OPENSTACK_VOLUMES_JSON_KEY

RESOURCE_TYPE_MAPPINGS = {
    OPENSTACK_SECURITY_GROUPS_JSON_KEY: "security_group",
    OPENSTACK_INSTANCES_JSON_KEY: "instance",
    OPENSTACK_NETWORKS_JSON_KEY: "network",
    OPENSTACK_VOLUMES_JSON_KEY: "volume"
}


def ensure_indexed_by_type(information_as_json: Dict):
    """
    TODO
    :param information_as_json:
    :return:
    """
    if not is_indexed_by_type(information_as_json):
        raise ValueError("Can only re-index information already indexed by type")


def is_indexed_by_type(information_as_json: Dict) -> bool:
    """
    Checks whether the given OpenStack information is indexed by type.
    :param information_as_json: the OpenStack information as JSON
    :return:
    """
    for key in RESOURCE_TYPE_MAPPINGS.keys():
        if key not in information_as_json:
            return False
    return True


def index_information_by_id(information_as_json: Dict) -> Dict:
    """
    Creates an alternate view of the information, where resources are indexed by ID and contain their type as a
    property.
    :param information_as_json: the OpenStack information as JSON, indexed by type
    :return: ID indexed information
    """
    ensure_indexed_by_type(information_as_json)

    typed_resources: Dict = {}
    for type_key in information_as_json:
        resources_of_type = information_as_json[type_key]
        for resource in resources_of_type:
            resource["type"] = RESOURCE_TYPE_MAPPINGS[type_key]
            assert "id" in resource
            typed_resources[resource["id"]] = resource
    return typed_resources


def index_information_by_type(information_as_json: Dict) -> Dict:
    """
    TODO
    :param information_as_json:
    :return:
    """
    ensure_indexed_by_type(information_as_json)
    return information_as_json
