from abc import ABCMeta, abstractmethod

from typing import Dict

from openstackinfo.schema import ID_JSON_KEY, TYPE_JSON_KEY, RESOURCE_TYPE_MAPPINGS, \
    ValidationError, IndexedByTypeValidator, IndexedByIdValidator, Validator


class UnsupportedIndexingError(ValueError):
    """
    Raised when the indexer cannot be used as the information is indexed already but in an unsupported way.
    """


class InformationIndexer(metaclass=ABCMeta):
    """
    Indexes information in a way defined by this class.
    """
    @abstractmethod
    def index(self, information: Dict):
        """
        Index the given information in the way defined by this class.
        :param information: the information to index (not modified)
        :return: the indexed information
        """

    def ensure_valid(self, information: Dict, validator: Validator):
        """
        Ensures that the given information validates with the given validator else it cannot be indexed.
        :param information: to check
        :param validator: to perform the validation
        :raises CannotIndexInFormError: raised if the given information does not validate
        """
        try:
            validator.ensure_valid(information)
        except ValidationError:
            raise UnsupportedIndexingError(information)


class InformationIndexerById(InformationIndexer):
    """
    Indexes the information by ID.
    """
    def index(self, information: Dict):
        self.ensure_valid(information, IndexedByTypeValidator())
        typed_resources: Dict = {}
        for type_key in information:
            resources_of_type = information[type_key]
            for resource in resources_of_type:
                resource[TYPE_JSON_KEY] = RESOURCE_TYPE_MAPPINGS[type_key]
                assert ID_JSON_KEY in resource
                typed_resources[resource[ID_JSON_KEY]] = resource
        assert IndexedByIdValidator().get_validity(typed_resources)
        return typed_resources


class InformationIndexerByType(InformationIndexer):
    """
    Indexes the information by type.
    """
    def index(self, information: Dict):
        self.ensure_valid(information, IndexedByTypeValidator())
        return information

