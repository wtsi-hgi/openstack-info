from abc import ABCMeta, abstractmethod

from typing import Dict, Tuple

ID_JSON_KEY = "id"
TYPE_JSON_KEY = "type"

OPENSTACK_IMAGES_JSON_KEY = "images"
OPENSTACK_INSTANCES_JSON_KEY = "instances"
OPENSTACK_KEYPAIRS_JSON_KEY = "keypairs"
OPENSTACK_NETWORKS_JSON_KEY = "networks"
OPENSTACK_SECURITY_GROUPS_JSON_KEY = "security_groups"
OPENSTACK_SUBNETS_JSON_KEY = "subnets"
OPENSTACK_ROUTERS_JSON_KEY = "routers"
OPENSTACK_VOLUMES_JSON_KEY = "volumes"

RESOURCE_TYPE_MAPPINGS = {
    OPENSTACK_IMAGES_JSON_KEY: "image",
    OPENSTACK_INSTANCES_JSON_KEY: "instance",
    OPENSTACK_KEYPAIRS_JSON_KEY: "keypair",
    OPENSTACK_NETWORKS_JSON_KEY: "network",
    OPENSTACK_SECURITY_GROUPS_JSON_KEY: "security_group",
    OPENSTACK_SUBNETS_JSON_KEY: "subnet",
    OPENSTACK_ROUTERS_JSON_KEY: "router",
    OPENSTACK_VOLUMES_JSON_KEY: "volume"

}


class ValidationError(ValueError):
    """
    Raised if the validation against a schema fails.
    """


class Validator(metaclass=ABCMeta):
    """
    Validates information formatted as JSON.
    """
    def ensure_valid(self, information: Dict):
        """
        Validates the given information against this validator.
        :param information: to be validated
        :raises ValidationError: if information does not validate
        """
        valid, reason = self.get_validity(information)
        if not valid:
            raise ValidationError(reason)

    def is_valid(self, information: Dict) -> bool:
        """
        Checks whether the given information is valid.
        :param information: to validate
        :return: `True` if valid
        """
        return self.get_validity(information)[0]

    @abstractmethod
    def get_validity(self, information: Dict) -> Tuple[bool, str]:
        """
        Gets the validity of the information, along with a reasoning for this (if any).
        :param information:
        :return: tuple where the first element is a boolean, where `True` indicates the information is valid and the
        second element is a human readable string indicating why the information is valid or not
        """


class IndexedByTypeValidator(Validator):
    """
    Validates whether information is indexed by type.
    """
    def get_validity(self, information: Dict):
        for key, value in information.items():
            if key not in RESOURCE_TYPE_MAPPINGS:
                return False, f"Unexpected key \"{key}\": {information}"
            elif not isinstance(value, list):
                return False, f"Unexpected value type associated to key - expected `list`, found `{type(value)}`: " \
                              f"{information}"
        return True, None


class IndexedByIdValidator(Validator):
    """
    Validates whether information is indexed by ID.
    """
    def get_validity(self, information: Dict):
        for key, resource in information.items():
            if not isinstance(resource, dict):
                return False, f"Expected resource represented as dict: {information}"
            if key != resource[ID_JSON_KEY]:
                return False, f"ID on index key does not match: {information}"
        return True, None
