from typing import Dict

from openstackinfo.models import RunConfiguration


def get_information(configuration: RunConfiguration) -> Dict:
    """
    Runs the given confirmation to get information about OpenStack tenant.
    :param configuration: run configuration
    :return: information about OpenStack tenant
    """
    openstack_info = configuration.retriever.get_openstack_info()
    indexed_openstack_info = configuration.indexer().index(openstack_info)
    return indexed_openstack_info

