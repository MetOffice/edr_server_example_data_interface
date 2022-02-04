from collections import namedtuple
from collections import namedtuple
from typing import Dict, List

from edr_server.abstract_data_interface.admin import RefreshCollections


PARAMS = {
    "a": [
        "xxxxa",
        "A dummy parameter A with certain characteristics",
        "Dummy ratio",
        "0.5",
        "http://www.example.com/define/dummy_ratio",
        "http://www.example.com/define/property/a",
        "A dummy parameter A",
    ],
    "b": [
        "xxxxb",
        "A dummy parameter B with special characteristics",
        "Dummy value",
        "1000",
        "http://www.example.com/define/dummy_value",
        "http://www.example.com/define/property/b",
        "A dummy parameter B",
    ],
    "c": [
        "xxxxc",
        "A dummy parameter C with specific characteristics",
        "Dummy constant",
        "1",
        "http://www.example.com/define/dummy_constant",
        "http://www.example.com/define/property/c",
        "A dummy parameter C",
    ],
}

PARAMS_LOOKUP = {
    "00001": ["a", "c"],
    "00002": ["a", "b", "c"],
}

SAMPLES: Dict = {
    "00001": [
        "00001",
        "One",
        "The first item",
        "CRS84",
        "WGS 1984",
        [-180, -90, 180, 90],
        ["Example", "Dummy"],
    ],
    "00002": [
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

PARAM_FIELDS = [
    "name",
    "id",
    "description",
    "unit_label",
    "unit_value",
    "unit_defn",
    "property_id",
    "property_label"
]

param = namedtuple("param", PARAM_FIELDS)


class RefreshCollections(RefreshCollections):
    def __init__(self, supported_data_queries) -> None:
        super().__init__(supported_data_queries)
        self.collection = namedtuple("collection", FIELDS)

    def _get_temporal_extent(self):
        this_extent = True
        if this_extent:
            FIELDS.extend(["temporal_interval", "trs", "temporal_name"])
            SAMPLES["00001"].extend(["today", "TIMECRS", "Dummy temporal extent"])
            SAMPLES["00002"].extend(["today/tomorrow", "TIMECRS", "Dummy temporal extent"])
        self.temporal_extent = this_extent

    def _get_vertical_extent(self):
        this_extent = True
        if this_extent:
            FIELDS.extend(["vertical_interval", "vrs", "vertical_name"])
            SAMPLES["00001"].extend([[2], "VERTCS", "Dummy vertical extent"])
            SAMPLES["00002"].extend([[2, 10], "VERTCS", "Dummy vertical extent"])
        self.vertical_extent = this_extent

    def get_parameters(self, collection_id):
        param_names = PARAMS_LOOKUP[collection_id]
        params = {}
        for name in param_names:
            param_metadata = PARAMS[name]
            params[name] = param(name, *param_metadata)
        return params

    def make_collection(self, name):
        sample = SAMPLES[name]
        return self.collection(*sample)

    def make_collections(self) -> List:
        collections: List = []
        for name in SAMPLES.keys():
            collection = self.make_collection(name)
            collections.append(collection)
        return collections