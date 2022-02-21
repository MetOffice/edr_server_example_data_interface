from typing import List

from shapely.geometry import box, Point, Polygon

from edr_server.abstract_data_interface.locations import Location, Locations, Parameter


CATEGORY_ENCODING = {
    "#000": 0.0,
    "#444": 20.0,
    "#888": 40.0,
    "#ccc": 60.0,
    "#fff": 80.0,
}


PARAMETERS = {
    "param1": {
        "name": "Parameter 1",
        "description": "The first parameter, describing wind speed",
        "unit": "m s-1",
        "unit_label": "m/s",
        "unit_type": "http://www.example.com/define/unit/ms-1",
        "phenomenon_id": "http://www.example.com/phenom/wind_speed",
        "phenomenon": "Wind Speed",
        "category_encoding": CATEGORY_ENCODING,
    },
    "param2": {
        "name": "Parameter 2",
        "description": "The second parameter, describing geopotential height",
        "unit": "m",
        "unit_label": "m",
        "unit_type": "http://www.example.com/define/unit/m",
        "phenomenon_id": "http://www.example.com/phenom/geo_height",
        "phenomenon": "Geopotential Height",
    },
    "param3": {
        "name": "Parameter 3",
        "description": "The third parameter, describing average hourly wind speed",
        "unit": "m s-1",
        "unit_label": "m/s",
        "unit_type": "http://www.example.com/define/unit/ms-1",
        "phenomenon_id": "http://www.example.com/phenom/wind_speed_mean",
        "phenomenon": "Mean Average Wind Speed",
        "measurement_type_method": "average",
        "measurement_type_period": "PT1H",
        "category_encoding": CATEGORY_ENCODING,
    },
}


LOCATIONS = {
    50232: [
        Point(51, -3),
        {
            "name": "Point",
            "datetime": "2021-01-31T00:00:00Z",
            "detail": "http://www.example.com/define/location/50232",
            "description": "A point location",
        },
    ],
    61812: [
        Polygon([[51, -3], [51, 0], [54, 0], [51, -3]]),
        {
            "name": "Polygon",
            "datetime": "2020-08-15T12:30:00Z",
            "detail": "http://www.example.com/define/location/61812",
            "description": "A polygon",
        },
    ],
    61198: [
        Point(25, -120),
        {
            "name": "Timeseries",
            "datetime": "2021-01-01T00:00:00Z/2021-02-01T00:00:00Z",
            "detail": "http://www.example.com/define/location/61198",
            "description": "A point location over a timeseries",
        },
    ],
}


LOCATIONS_LOOKUP = {
    "00001": [50232],
    "00002": [50232, 61812, 61198],
}


PARAMETERS_LOOKUP = {
    50232: ["param1", "param2", "param3"],
    61812: ["param2"],
    61198: ["param1", "param2", "param3"],
}


class Locations(Locations):
    def __init__(self, collection_id, query_parameters: dict) -> None:
        super().__init__(collection_id, query_parameters)
        self._parameters = self.parameters()

    def _bbox_filter(self, location: Location) -> bool:
        bbox_extent = self.query_parameters["bbox"]
        bbox = box(
            bbox_extent["xmin"], bbox_extent["ymin"], bbox_extent["xmax"], bbox_extent["ymax"]
        )
        geometry = LOCATIONS[location.id][0]
        return bbox.intersects(geometry)

    def _datetime_filter(self, location: Location) -> bool:
        return True

    def locations_filter(self, locations):
        """Filter locations by collection ID and any request query parameters."""
        collection_location_ids = LOCATIONS_LOOKUP[self.collection_id]
        locations = filter(
            lambda l: l.id in collection_location_ids,
            locations)
        if self.query_parameters.get("bbox") is not None:
            locations = filter(self._bbox_filter, locations)
        if self.query_parameters.get("datetime") is not None:
            locations = filter(self._datetime_filter, locations)
        return list(locations)

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
        bbox = geometry.bounds
        return geom_type, coords, bbox

    def _handle_location(self, loc):
        geometry, properties = loc
        geom_type, coords, bbox = self._handle_geometry(geometry)
        return geom_type, coords, bbox, properties

    def parameters(self) -> List[Parameter]:
        params = []
        for id, metadata in PARAMETERS.items():
            param = Parameter(id, **metadata)
            params.append(param)
        return params

    def all_locations(self) -> List[Location]:
        locs_list = []
        for key, loc_metadata in LOCATIONS.items():
            geometry_type, coord_list, bbox, properties = self._handle_location(loc_metadata)
            location_parameter_ids = PARAMETERS_LOOKUP[key]
            loc_parameters = filter(lambda param: param.id in location_parameter_ids, self._parameters)
            loc = Location(**{
                "id": key,
                "geometry_type": geometry_type,
                "coords": coord_list,
                "bbox": bbox,
                "temporal_interval": "",
                "properties": properties,
                "parameters": list(loc_parameters),
                "referencing": [],
            })
            locs_list.append(loc)
        return locs_list

    def get_collection_bbox(self):
        from .admin import SAMPLES
        return SAMPLES[self.collection_id][-2]