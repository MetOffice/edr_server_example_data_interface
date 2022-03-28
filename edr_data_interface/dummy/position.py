from itertools import chain
from typing import List, Union

from shapely.geometry import box

from edr_server.abstract_data_interface.position import Position
from edr_server.abstract_data_interface.locations import Feature

from .import filters
from .items import Items


class Position(Position):
    filter_type = "intersection"

    def _exact_match(self):
        """Return only items that are at the exact location specified."""
        pass

    def _fuzzy_match(self, fuzz=1):
        """Return items that are at the location specified, within a small tolerance."""
        pass

    def all_items(self) -> List[Feature]:
        items_provider = Items(self.collection_id, self.query_parameters, "")
        items = items_provider.get_features()
        return list(chain.from_iterable(items.values()))

    def polygon_filter(self, items: List[Feature]) -> Union[List[Feature], None]:
        """
        Implement a polygon filter that tests for the polygon provided in the
        query arguments intersecting with the feature's bounding box.

        """
        # XXX implement!
        pass
