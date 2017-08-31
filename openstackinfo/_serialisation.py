from hgijson import JsonPropertyMapping, MappingJSONEncoderClassBuilder
from openstack.block_store.v2.volume import VolumeDetail
from openstack.compute.v2.server import ServerDetail
from openstack.network.v2.network import Network
from openstack.network.v2.security_group import SecurityGroup

from openstackinfo.models import Openstack

ID_JSON_KEY = "id"
NAME_JSON_KEY = "id"

OPENSTACK_INSTANCES_JSON_KEY = "instances"
OPENSTACK_VOLUMES_JSON_KEY = "volumes"
OPENSTACK_NETWORKS_JSON_KEY = "networks"
OPENSTACK_SECURITY_GROUPS_JSON_KEY = "security_groups"

NETWORK_SUBNET_IDS_JSON_KEY = "subnet_ids"

VOLUME_ATTACHED_TO_JSON_KEY = "attached_to"

SERVER_NETWORKS_JSON_KEY = "networks"
SERVER_VOLUMES_JSON_KEY = "volumes_attached"
SERVER_STATUS_JSON_KEY = "status"
SERVER_CREATED_AT_JSON_KEY = "created"
SERVER_UPDATED_AT_JSON_KEY = "updated"
SERVER_SECURITY_GROUPS_JSON_KEY = "security_groups"
SERVER_METADATA_JSON_KEY = "metadata"


network_mapping_schema = [
    JsonPropertyMapping(ID_JSON_KEY, "id"),
    JsonPropertyMapping(NAME_JSON_KEY, "name"),
    JsonPropertyMapping(NETWORK_SUBNET_IDS_JSON_KEY, "subnet_ids")
]
NetworkJSONEncoder = MappingJSONEncoderClassBuilder(Network, network_mapping_schema).build()


volume_mapping_schema = [
    JsonPropertyMapping(ID_JSON_KEY, "id"),
    JsonPropertyMapping(NAME_JSON_KEY, "name"),
    JsonPropertyMapping(VOLUME_ATTACHED_TO_JSON_KEY,
                        object_property_getter=lambda volume: [attachment["server_id"] for attachment
                                                               in volume.attachments])
]
VolumeJSONEncoder = MappingJSONEncoderClassBuilder(VolumeDetail, volume_mapping_schema).build()


security_group_mapping_schema = [
    JsonPropertyMapping(ID_JSON_KEY, "id"),
    JsonPropertyMapping(NAME_JSON_KEY, "name")
]
SecurityGroupJSONEncoder = MappingJSONEncoderClassBuilder(SecurityGroup, security_group_mapping_schema).build()


server_mapping_schema = [
    JsonPropertyMapping(ID_JSON_KEY, "id"),
    JsonPropertyMapping(NAME_JSON_KEY, "name"),
    JsonPropertyMapping(SERVER_NETWORKS_JSON_KEY, "networks"),
    JsonPropertyMapping(SERVER_VOLUMES_JSON_KEY, object_property_getter=lambda server: [volume["id"] for volume in server.attached_volumes]),
    JsonPropertyMapping(SERVER_STATUS_JSON_KEY, "status"),
    JsonPropertyMapping(SERVER_CREATED_AT_JSON_KEY, "created_at"),
    JsonPropertyMapping(SERVER_UPDATED_AT_JSON_KEY, "updated_at"),
    JsonPropertyMapping(SERVER_SECURITY_GROUPS_JSON_KEY, object_property_getter=lambda server: [group.id for group in server.security_groups]),
    JsonPropertyMapping(SERVER_METADATA_JSON_KEY, "metadata")
]
ServerJSONEncoder = MappingJSONEncoderClassBuilder(ServerDetail, server_mapping_schema).build()


openstack_mapping_schema = [
    JsonPropertyMapping(OPENSTACK_INSTANCES_JSON_KEY, "servers", encoder_cls=ServerJSONEncoder),
    JsonPropertyMapping(OPENSTACK_VOLUMES_JSON_KEY, "volumes", encoder_cls=VolumeJSONEncoder),
    JsonPropertyMapping(OPENSTACK_SECURITY_GROUPS_JSON_KEY, "security_groups", encoder_cls=SecurityGroupJSONEncoder),
    JsonPropertyMapping(OPENSTACK_NETWORKS_JSON_KEY, "networks", encoder_cls=NetworkJSONEncoder)
]
OpenstackJSONEncoder = MappingJSONEncoderClassBuilder(Openstack, openstack_mapping_schema).build()
