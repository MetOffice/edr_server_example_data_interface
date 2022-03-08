import copy
from typing import List

from edr_server.abstract_data_interface.admin import Collection, RefreshCollections
from edr_server.abstract_data_interface.locations import Parameter

from . import dataset


class RefreshCollections(RefreshCollections):
    def __init__(self, supported_data_queries) -> None:
        super().__init__(supported_data_queries)

    def _get_temporal_extent(self, name):
        extents = dataset.TEMPORAL_EXTENTS[name]
        if not len(extents["temporal_interval"]):
            extents = None
        return extents

    def _get_vertical_extent(self, name):
        extents = dataset.VERTICAL_EXTENTS[name]
        if not len(extents["vertical_interval"]):
            extents = None
        return extents

    def get_parameters(self, collection_id) -> List[Parameter]:
        param_names = dataset.PARAMETERS_COLLECTIONS_LOOKUP[collection_id]
        params = []
        for name in param_names:
            param_metadata = dataset.PARAMETERS[name]
            params.append(Parameter(name, **param_metadata))
        return params

    def make_collection(self, name) -> Collection:
        coll = copy.copy(dataset.COLLECTIONS[name])
        t_extents = self._get_temporal_extent(name)
        if t_extents is not None:
            coll.update(t_extents)
        v_extents = self._get_vertical_extent(name)
        if v_extents is not None:
            coll.update(v_extents)
        return Collection(**coll)

    def make_collections(self) -> List[Collection]:
        collections: List = []
        for name in dataset.COLLECTIONS.keys():
            collection = self.make_collection(name)
            collections.append(collection)
        return collections