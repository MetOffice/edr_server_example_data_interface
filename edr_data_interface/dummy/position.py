from itertools import chain
from typing import List, Union

from shapely.geometry import box
import shapely.wkt as wkt

from edr_server.abstract_data_interface.position import Position
from edr_server.abstract_data_interface.locations import Feature

from .items import Items


class Position(Position):
    n_filtered = 0

    def _determine_handler_type(self) -> str:
        return "domain" if self.n_filtered == 1 else "feature_collection"

    def _exact_match(self, point, item):
        """Return only items that are at the exact location specified."""
        if item.geometry_type != "point":
            # We can't exactly point-match if we don't have two points.
            return self._fuzzy_match(point, item)
        else:
            item_point = wkt.loads(f"{item.geometry_type}({float(item.coords[0])} {float(item.coords[1])})")
            return point == item_point

    def _fuzzy_match(self, point, item):
        """Return items that are at the location specified, within a small tolerance defined by `self.fuzz`."""
        xlo, ylo, xhi, yhi = item.bbox
        fuzzy_geom = box(xlo-self.fuzz, ylo-self.fuzz, xhi+self.fuzz, yhi+self.fuzz)
        return point.intersects(fuzzy_geom)

    def _matcher(self, point, items):
        meth = self._exact_match if self.match == "exact" else self._fuzzy_match
        filtered = filter(lambda item: meth(point, item), items)
        return list(filtered)

    def get_collection_bbox(self):
        from .dataset import COLLECTIONS
        return COLLECTIONS[self.collection_id]["bbox"]

    def all_items(self) -> List[Feature]:
        items_provider = Items(self.collection_id, self.query_parameters, "")
        items = items_provider.get_features()
        return list(chain.from_iterable(items.values()))

    def polygon_filter(self, items: List[Feature]) -> Union[List[Feature], None]:
        """
        Implement a polygon filter that tests for the polygon provided in the
        query arguments intersecting with the feature's bounding box.

        """
        self.fuzz = 0.1
        self.match = "exact"

        result = None
        geometry = self.query_parameters.get("coords")
        if geometry.geom_type.lower() == "point":
            result = self._matcher(geometry, items)
        else:
            # We confirmed in `self._check_query_args` that we only had Point/MultiPoint.
            result = []
            for point in geometry.geoms:
                result.extend(self._matcher(point, items))
        self.n_filtered = len(result)
        return result
