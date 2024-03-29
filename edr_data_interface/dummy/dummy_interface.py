from edr_server.core.exceptions import CollectionNotFoundException
from edr_server.core.interface import AbstractCollectionsMetadataDataInterface, EdrRequest
from edr_server.core.models import CollectionId
from edr_server.core.models.metadata import CollectionMetadataList, CollectionMetadata

from . import area, capabilities, dataset, filters, items, locations, position, radius, service


class DummyCollectionsMetadataDataInterface(AbstractCollectionsMetadataDataInterface):
    def all(self, request: EdrRequest) -> CollectionMetadataList:
        return CollectionMetadataList(list(dataset.COLLECTIONS.values()))

    def get(self, collection_id: CollectionId, request: EdrRequest) -> CollectionMetadata:
        try:
            return dataset.COLLECTIONS[collection_id]
        except KeyError:
            raise CollectionNotFoundException(f"Collection {collection_id!r} doesn't exist")


class DummyEdrDataInterface:
    """
    A patched version of EdrDataInterface whilst we're updating the data interface and transitioning this dummy
    implementation to use it
    """

    collections = DummyCollectionsMetadataDataInterface()
    Area = area.Area
    Capabilities = capabilities.Capabilities
    filters = filters
    Items = items.Items
    Item = items.Item
    Location = locations.Location
    Locations = locations.Locations
    Position = position.Position
    Radius = radius.Radius
    Service = service.Service
