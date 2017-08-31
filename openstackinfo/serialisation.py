from hgijson import JsonPropertyMapping, MappingJSONEncoderClassBuilder
from novaclient.v2.servers import SecurityGroup as NovaSecurityGroup
from openstack.block_store.v2.volume import VolumeDetail
from openstack.compute.v2.server import ServerDetail
from openstack.network.v2.network import Network
from openstack.network.v2.security_group import SecurityGroup

from openstackinfo.models import Openstack


network_mapping_schema = [
    JsonPropertyMapping("id", "id"),
    JsonPropertyMapping("name", "name"),
    JsonPropertyMapping("subnet_ids", "subnet_ids")
]
NetworkJSONEncoder = MappingJSONEncoderClassBuilder(Network, network_mapping_schema).build()


volume_mapping_schema = [
    JsonPropertyMapping("id", "id"),
    JsonPropertyMapping("name", "name"),
    JsonPropertyMapping("attached_to", object_property_getter=lambda volume: [attachment["server_id"] for attachment
                                                                              in volume.attachments])
]
VolumeJSONEncoder = MappingJSONEncoderClassBuilder(VolumeDetail, volume_mapping_schema).build()


security_group_mapping_schema = [
    JsonPropertyMapping("id", "id"),
    JsonPropertyMapping("name", "name")
]
SecurityGroupJSONEncoder = MappingJSONEncoderClassBuilder(SecurityGroup, security_group_mapping_schema).build()


server_mapping_schema = [
    JsonPropertyMapping("id", "id"),
    JsonPropertyMapping("name", "name"),
    JsonPropertyMapping("networks", "networks"),
    JsonPropertyMapping("volumes_attached", object_property_getter=lambda server: [volume["id"] for volume in server.attached_volumes]),
    JsonPropertyMapping("status", "status"),
    JsonPropertyMapping("created", "created_at"),
    JsonPropertyMapping("updated", "updated_at"),
    JsonPropertyMapping("security_groups", object_property_getter=lambda server: [group.id for group in server.security_groups]),
    JsonPropertyMapping("metadata", "metadata")
]
ServerJSONEncoder = MappingJSONEncoderClassBuilder(ServerDetail, server_mapping_schema).build()


openstack_mapping_schema = [
    JsonPropertyMapping("instances", "servers",  encoder_cls=ServerJSONEncoder),
    JsonPropertyMapping("volumes", "volumes",  encoder_cls=VolumeJSONEncoder),
    JsonPropertyMapping("security_groups", "security_groups",  encoder_cls=SecurityGroupJSONEncoder),
    JsonPropertyMapping("networks", "networks",  encoder_cls=NetworkJSONEncoder)
]
OpenstackJSONEncoder = MappingJSONEncoderClassBuilder(Openstack, openstack_mapping_schema).build()
