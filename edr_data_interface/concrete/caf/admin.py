from typing import List

from clean_air.data.storage import S3FSMetadataStore
from clean_air.models import Metadata

from ...abstract.admin import RefreshCollections


class RefreshCollections(RefreshCollections):
    def __init__(self):
        self.metadata_store = S3FSMetadataStore

    def collection(self, name) -> Metadata:
        return self.metadata_store.get(name)

    def collections(self) -> List:
        collections_metadata: List[Metadata] = []
        for collection_name in self.metadata_store.available_datasets():
            collection_metadata = self.collection(collection_name)
            collections_metadata.append(collection_metadata)
        return collections_metadata