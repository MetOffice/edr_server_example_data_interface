from typing import List

from shapely.geometry import Point, Polygon

from edr_server.abstract_data_interface.locations import Location, Locations


LOCATIONS = {
    50232: [
        Point(51, -3),
        {
            "name": "Point",
            "datetime": "2021-01-31T00:00:00Z",
            "detail": "http://www.example.com/define/location/50232",
            "description": "A point location"
        },
    ],
    61812: [
        Polygon([[51, -3], [51, 0], [54, 0], [51, -3]]),
        {
            "name": "Polygon",
            "datetime": "2020-08-15T12:30:00Z",
            "detail": "http://www.example.com/define/location/61812",
            "description": "A polygon"
        },
    ],
    61198: [
        Point(25, -120),
        {
            "name": "Timeseries",
            "datetime": "2021-01-01T00:00:00Z/2021-02-01T00:00:00Z",
            "detail": "http://www.example.com/define/location/61198",
            "description": "A point location over a timeseries"
        },
    ],
}


LOCATIONS_LOOKUP = {
    "00001": [50232],
    "00002": [50232, 61812, 61198],
}


class Locations(Locations):
    def locations_filter(self, locations):
        """Filter locations by collection ID and any request query parameters."""
        collection_location_ids = LOCATIONS_LOOKUP[self.collection_id]
        collection_locations = filter(
            lambda l: l.id in collection_location_ids,
            locations)
        # TODO add query parameter filters.
        return list(collection_locations)

    def _handle_geometry(self, geometry):
        """
        Extract the geometry type (Point, LineString etc) and coordinate points
        from `geometry`.

        """
        geom_type = geometry.__class__.__name__
        if geom_type == "Polygon":
            points = list(geometry.exterior.coords)
        else:
            points = list(geometry.coords)
        if len(points) == 1:
            # Coords from all types of geometry are returned as a list of tuples.
            # If there's only one tuple, we just want the tuple, not the list too.
            coords = points[0]
        else:
            # Otherwise, we want to covert each tuple into a space-separated string
            # of coordinate points.
            coords = [" ".join([str(emt) for emt in coord]) for coord in points]
        return geom_type, coords

    def _handle_location(self, loc):
        geometry, properties = loc
        geom_type, coords = self._handle_geometry(geometry)
        return geom_type, coords, properties

    def all_locations(self) -> List[Location]:
        locs_list = []
        for key, loc_metadata in LOCATIONS.items():
            geometry_type, coord_list, properties = self._handle_location(loc_metadata)
            loc = Location(**{
                "id": key,
                "geometry_type": geometry_type,
                "coords": coord_list,
                "properties": properties,
            })
            locs_list.append(loc)
        return locs_list