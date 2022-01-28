from collections import namedtuple
from collections import namedtuple
from typing import Dict, List

from ...abstract.admin import RefreshCollections


SAMPLES: Dict = {
    "one": [
        "00001",
        "One",
        "The first item",
        "CRS84",
        "WGS 1984",
        [-180, -90, 180, 90],
        ["Example", "Dummy"],
    ],
    "two": [
        "00002",
        "Two",
        "The second item",
        "EPSG4326",
        "EPSG4326",
        [-180, -90, 180, 90],
        ["Example", "Dummy"],
    ],
}

FIELDS: List[str] = [
    "id",
    "name",
    "description",
    "crs",
    "crs_name",
    "bbox",
    "keywords",
]


class RefreshCollections(RefreshCollections):
    def __init__(self, supported_data_queries) -> None:
        super().__init__(supported_data_queries)
        self.collection = namedtuple("collection", FIELDS)

    def _get_temporal_extent(self):
        this_extent = True
        if this_extent:
            FIELDS.extend(["temporal_interval", "trs", "temporal_name"])
            SAMPLES["one"].extend(["today", "TIMECRS", "Dummy temporal extent"])
            SAMPLES["two"].extend(["today/tomorrow", "TIMECRS", "Dummy temporal extent"])
        self.temporal_extent = this_extent

    def _get_vertical_extent(self):
        this_extent = True
        if this_extent:
            FIELDS.extend(["vertical_interval", "vrs", "vertical_name"])
            SAMPLES["one"].extend([[2], "VERTCS", "Dummy vertical extent"])
            SAMPLES["two"].extend([[2, 10], "VERTCS", "Dummy vertical extent"])
        self.vertical_extent = this_extent

    def make_collection(self, name):
        sample = SAMPLES[name]
        return self.collection(*sample)

    def make_collections(self) -> List:
        collections: List = []
        for name in SAMPLES.keys():
            collection = self.make_collection(name)
            collections.append(collection)
        return collections