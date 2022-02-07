from collections import namedtuple
import copy
from typing import Dict, List

from edr_server.abstract_data_interface.admin import Collection, Parameter, RefreshCollections


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
        "One",
        "00001",
        "The first item",
        ["Example", "Dummy"],
        [-180, -90, 180, 90],
        "CRS84",
        "WGS 1984",
    ],
    "00002": [
        "Two",
        "00002",
        "The second item",
        ["Example", "Dummy"],
        [-180, -90, 180, 90],
        "EPSG4326",
        "EPSG4326",
    ],
}

TEMPORAL_EXTENTS: Dict = {
    "00001": [
        ["2010-06-30T00:00:00Z", "2010-06-30T00:00:00Z"],
        [],
        "TIMECRS",
        "Dummy temporal extent"],
    "00002": [
        ["2015-11-01T00:00:00", "2015-11-02T00:00:00"],
        ["R24/2015-11-02T00:00:00/PT1H"],
        "TIMECRS",
        "Dummy temporal extent"],
}

VERTICAL_EXTENTS: Dict = {
    "00001": [[], [], "VERTCS", "Empty dummy vertical extent"],
    "00002": [
        ["2", "10"],
        ["2", "3", "4", "5", "6", "7", "8", "9", "10"],
        "VERTCS",
        "Dummy vertical extent",
    ],
}

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

    def _get_temporal_extent(self, name):
        this_extent = True
        extents = TEMPORAL_EXTENTS[name] if this_extent else None
        return extents

    def _get_vertical_extent(self, name):
        this_extent = True
        extents = VERTICAL_EXTENTS[name] if this_extent else None
        return extents

    def get_parameters(self, collection_id) -> List[Parameter]:
        param_names = PARAMS_LOOKUP[collection_id]
        params = []
        for name in param_names:
            param_metadata = PARAMS[name]
            params.append(Parameter(name, *param_metadata))
        return params

    def make_collection(self, name) -> Collection:
        sample = copy.copy(SAMPLES[name])
        t_extents = self._get_temporal_extent(name)
        if t_extents is not None:
            sample.extend(t_extents)
        v_extents = self._get_vertical_extent(name)
        if v_extents is not None:
            sample.extend(v_extents)
        return Collection(*sample)

    def make_collections(self) -> List[Collection]:
        collections: List = []
        for name in SAMPLES.keys():
            collection = self.make_collection(name)
            collections.append(collection)
        return collections