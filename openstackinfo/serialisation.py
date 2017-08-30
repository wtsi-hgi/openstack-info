from hgijson import JsonPropertyMapping, MappingJSONEncoderClassBuilder
from novaclient.v2.servers import Server, SecurityGroup

security_group_mapping_schema = [
    JsonPropertyMapping("id", "id"),
    JsonPropertyMapping("name", "name"),
]
SecurityGroupJSONEncoder = MappingJSONEncoderClassBuilder(SecurityGroup, security_group_mapping_schema).build()


server_mapping_schema = [
    JsonPropertyMapping("id", "id"),
    JsonPropertyMapping("name", "name"),
    JsonPropertyMapping("networks", "networks"),
    JsonPropertyMapping("volumes_attached", object_property_getter=lambda server: [volume["id"] for volume in getattr(
        server, "os-extended-volumes:volumes_attached")]),
    JsonPropertyMapping("status", "status"),
    JsonPropertyMapping("created", "created"),
    JsonPropertyMapping("updated", "updated"),
    JsonPropertyMapping("security_groups", "security_groups", encoder_cls=SecurityGroupJSONEncoder),
    JsonPropertyMapping("metadata", "metadata"),
]
ServerJSONEncoder = MappingJSONEncoderClassBuilder(Server, server_mapping_schema).build()
