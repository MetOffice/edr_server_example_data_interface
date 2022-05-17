from edr_server.core import EdrDataInterface, AbstractCollectionsMetadataDataInterface, CollectionId, \
    CollectionMetadata, CollectionMetadataList
from edr_server.core.exceptions import CollectionNotFoundException
from . import area
from . import capabilities
from . import filters
from . import items
from . import locations
from . import position
from . import radius
from . import service


class DummyCollectionsMetadataDataInterface(AbstractCollectionsMetadataDataInterface):
    def all(self) -> CollectionMetadataList:
        return CollectionMetadataList([])

    def get(self, collection_id: CollectionId) -> CollectionMetadata:
        raise CollectionNotFoundException


class DummyEdrDataInterface(EdrDataInterface):
    """
    A patched version of EdrDataInterface whilst we're updating the data interface and transitioning this dummy
    implementation to use it
    """

    collections = DummyCollectionsMetadataDataInterface()
    area = area
    capabilities = capabilities
    filters = filters
    items = items
    locations = locations
    position = position
    radius = radius
    service = service
