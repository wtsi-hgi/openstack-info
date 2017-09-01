from abc import ABCMeta

from typing import Dict

from openstackinfo.schema import ID_JSON_KEY, TYPE_JSON_KEY, RESOURCE_TYPE_MAPPINGS, validate, INDEX_BY_TYPE_SCHEMA, \
    ValidationError


class CannotIndexInFormError(ValueError):
    """
    Raised when the indexer cannot be used as the information is indexed already but in an unsupported way.
    """


class InformationIndexer(metaclass=ABCMeta):
    """
    Indexes information in a way defined by this class.
    """
    def index(self, information: Dict):
        """
        Index the given information in the way defined by this class.
        :param information: the information to index (not modified)
        :return: the indexed information
        """

    def ensure_information_schema(self, information: Dict, schema: Dict):
        """
        Ensures that the given information complies with the given schema in order for indexing to proceed.
        :param information: the information to check
        :param schema: the schema to enforce
        :raises CannotIndexInFormError: raised if the given information does not comply to the given schema
        """
        try:
            validate(information, schema)
        except ValidationError:
            raise CannotIndexInFormError(information)


class InformationIndexerById(InformationIndexer):
    """
    Indexes the information by ID.
    """
    def index(self, information: Dict):
        self.ensure_information_schema(information, INDEX_BY_TYPE_SCHEMA)
        typed_resources: Dict = {}
        for type_key in information:
            resources_of_type = information[type_key]
            for resource in resources_of_type:
                resource[TYPE_JSON_KEY] = RESOURCE_TYPE_MAPPINGS[type_key]
                assert ID_JSON_KEY in resource
                typed_resources[resource[ID_JSON_KEY]] = resource
        # assert self.ensure_information_schema(information, INDEX_BY_ID_SCHEMA)
        return typed_resources


class InformationIndexerByType(InformationIndexer):
    """
    Indexes the information by type.
    """
    def index(self, information: Dict):
        self.ensure_information_schema(information, INDEX_BY_TYPE_SCHEMA)
        return information

