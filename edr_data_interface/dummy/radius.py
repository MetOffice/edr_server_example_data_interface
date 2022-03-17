from itertools import chain
from typing import List

from edr_server.abstract_data_interface.radius import Radius
from edr_server.abstract_data_interface.locations import Feature

from .items import Items


class Radius(Radius):
    def all_items(self) -> List[Feature]:
        items_provider = Items(self.collection_id, self.query_parameters, "")
        items = items_provider.get_features()
        return list(chain.from_iterable(items.values()))

    def get_collection_bbox(self):
        from .dataset import COLLECTIONS
        return COLLECTIONS[self.collection_id]["bbox"]
