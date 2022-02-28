import copy
from typing import Dict, List

from edr_server.abstract_data_interface.admin import Collection, Parameter, RefreshCollections

from . import dataset


class RefreshCollections(RefreshCollections):
    def __init__(self, supported_data_queries) -> None:
        super().__init__(supported_data_queries)

    def _get_temporal_extent(self, name):
        this_extent = True
        extents = dataset.TEMPORAL_EXTENTS[name] if this_extent else None
        return extents

    def _get_vertical_extent(self, name):
        this_extent = True
        extents = dataset.VERTICAL_EXTENTS[name] if this_extent else None
        return extents

    def get_parameters(self, collection_id) -> List[Parameter]:
        param_names = dataset.PARAMS_LOOKUP[collection_id]
        params = []
        for name in param_names:
            param_metadata = dataset.PARAMS[name]
            params.append(Parameter(name, *param_metadata))
        return params

    def make_collection(self, name) -> Collection:
        sample = copy.copy(dataset.SAMPLES[name])
        t_extents = self._get_temporal_extent(name)
        if t_extents is not None:
            sample.extend(t_extents)
        v_extents = self._get_vertical_extent(name)
        if v_extents is not None:
            sample.extend(v_extents)
        return Collection(*sample)

    def make_collections(self) -> List[Collection]:
        collections: List = []
        for name in dataset.SAMPLES.keys():
            collection = self.make_collection(name)
            collections.append(collection)
        return collections