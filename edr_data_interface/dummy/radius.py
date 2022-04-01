from itertools import chain
from typing import List

from shapely.geometry import box

from edr_server.abstract_data_interface.radius import Radius
from edr_server.abstract_data_interface.locations import Feature

from .import filters
from .items import Items


class Radius(Radius):
    filter_type = "intersection"
    n_filtered = 0

    def _determine_handler_type(self) -> str:
        return "domain" if self.n_filtered == 1 else "feature_collection"

    def get_collection_bbox(self):
        from .dataset import COLLECTIONS
        return COLLECTIONS[self.collection_id]["bbox"]

    def all_items(self) -> List[Feature]:
        items_provider = Items(self.collection_id, self.query_parameters, "")
        items = items_provider.get_features()
        return list(chain.from_iterable(items.values()))

    def polygon_filter(self, items: List[Feature]) -> List[Feature]:
        """
        Implement a polygon filter that tests for the polygon provided in the
        query arguments intersecting with the feature's bounding box.

        """
        if self.filter_type == "intersection":
            result = filters.intersection_filter(self.polygon, items, self.items_url)
        elif self.filter_type == "cutout":
            result = filters.cutout_filter(self.polygon, items)
        else:
            raise ValueError(f"Filter type {self.filter_type!r} is not supported.")
        self.n_filtered = len(result)
        return result
