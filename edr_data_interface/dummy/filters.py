from typing import List

from edr_server.abstract_data_interface.locations import Feature
from shapely.geometry import box, Polygon


def cutout_filter(polygon: Polygon, items: List[Feature]):
    quick_filter_items = intersection_filter(polygon, items)
    # XXX more filtering here!
    return quick_filter_items


def intersection_filter(polygon: Polygon, items: List[Feature]) -> List[Feature]:
    """
    Implement a polygon filter that tests for `polygon` intersecting
    with the bounding box of each feature in `items`.

    """
    result = []
    for item in items:
        bbox = box(*item.bbox)
        if bbox.intersects(polygon):
            result.append(item)
    return result