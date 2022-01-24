from collections import namedtuple
from dataclasses import dataclass
from collections import namedtuple
from typing import Dict, List

from ...abstract.admin import RefreshCollections


SAMPLES: Dict = {
    "one": ["00001", "One", "The first item", "CRS84"],
    "two": ["00002", "Two", "The second item", "EPSG4326"],
}

FIELDS: List[str] = [
    "id",
    "name",
    "description",
    "crs",
]

collection = namedtuple("collection", FIELDS)


class RefreshCollections(RefreshCollections):
    def collection(self, name) -> collection:
        sample = SAMPLES[name]
        return collection(*sample)

    def collections(self) -> List[collection]:
        collections: List = []
        for name in SAMPLES.keys():
            collection = self.collection(name)
            collections.append(collection)
        return collections