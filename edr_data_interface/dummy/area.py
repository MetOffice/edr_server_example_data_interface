from itertools import chain
from typing import List

from shapely.geometry import box

from edr_server.abstract_data_interface.area import Area
from edr_server.abstract_data_interface.locations import Feature

from .items import Items


class Area(Area):
    def all_items(self) -> List[Feature]:
        items_provider = Items(self.collection_id, self.query_parameters, "")
        items = items_provider.get_features()
        return list(chain.from_iterable(items.values()))

    def get_collection_bbox(self):
        from .dataset import COLLECTIONS
        return COLLECTIONS[self.collection_id]["bbox"]

    def polygon_filter(self, items: List[Feature]) -> List[Feature]:
        """
        Implement a polygon filter that tests for the polygon provided in the
        query arguments intersecting with the feature's bounding box.

        """
        result = []
        for item in items:
            bbox = box(*item.bbox)
            if bbox.intersects(self.polygon):
                result.append(item)
        return result
