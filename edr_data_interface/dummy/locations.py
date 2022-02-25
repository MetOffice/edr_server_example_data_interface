from typing import List
from urllib.parse import urljoin

import numpy as np
from shapely.geometry import box, Point, Polygon

from edr_server.abstract_data_interface.locations import (
    Feature, Location, Locations, Parameter, Referencing, Tileset
)


def construct_data():
    x = y = np.arange(100)
    t = np.arange(1, 32)
    xm, ym = np.meshgrid(x, y)
    levels = [np.sin(0.5*xm + ti) + np.cos(0.2*ym + 2) for ti in t]
    return np.stack(levels)


CATEGORY_ENCODING = {
    "#000": 0.0,
    "#444": 20.0,
    "#888": 40.0,
    "#ccc": 60.0,
    "#fff": 80.0,
}


DATA = {
    "Parameter 1": np.array([2.4, 5.8, 3.1, 3.2]),
    "Parameter 2": construct_data(),
    "Parameter 3": np.array([4.3, 3.5, 6.2, 9.1])
}


PARAMETERS = {
    "Parameter 1": {
        "id": "param1",
        "description": "The first dummy parameter",
        "type": "NdArray",
        "dtype": DATA["Parameter 1"].dtype.name,
        "axes": ["t"],
        "shape": [4],
        "value_type": "values",
        "values": list(DATA["Parameter 1"]),
        "unit": "m s-1",
        "unit_label": "m/s",
        "unit_type": "http://www.example.com/define/unit/ms-1",
        "phenomenon_id": "http://www.example.com/phenom/dummy_1",
        "phenomenon": "Dummy 1",
        "category_encoding": CATEGORY_ENCODING,
    },
    "Parameter 2": {
        "id": "param2",
        "description": "The second dummy parameter",
        "type": "TiledNdArray",
        "dtype": DATA["Parameter 2"].dtype.name,
        "axes": ["t", "y", "x"],
        "shape": [31, 100, 100],
        "value_type": "tilesets",
        "values": [],
        "unit": "K",
        "unit_label": "K",
        "unit_type": "http://www.example.com/define/unit/K",
        "phenomenon_id": "http://www.example.com/phenom/dummy_2",
        "phenomenon": "Dummy 2",
    },
    "Parameter 3": {
        "id": "param3",
        "description": "The third dummy parameter",
        "type": "NdArray",
        "dtype": DATA["Parameter 3"].dtype.name,
        "axes": ["t"],
        "shape": [4],
        "value_type": "values",
        "values": list(DATA["Parameter 3"]),
        "unit": "m s-1",
        "unit_label": "m/s",
        "unit_type": "http://www.example.com/define/unit/ms-1",
        "phenomenon_id": "http://www.example.com/phenom/dummy_3",
        "phenomenon": "Dummy 3",
        "measurement_type_method": "average",
        "measurement_type_period": "PT6H",
        "category_encoding": CATEGORY_ENCODING,
    },
}


LOCATIONS = {
    "50232": {
        "geometry": Point(51, -3),
        "axes": ["t"],
        "axis_t_values": {"values": ["2021-01-31T00:00:00Z"]},
        "temporal_interval": "2021-01-31T00:00:00Z",
        "properties": {
            "name": "Point",
            "datetime": "2021-01-31T00:00:00Z",
            "detail": "http://www.example.com/define/location/50232",
            "description": "A point location",
        },
        "referencing": [
            {"coords": ["x", "y"], "system_type": "GeographicCRS", "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "standard"},
        ],
    },
    "61812": {
        "geometry": Polygon([[51, -3], [51, 0], [54, 0], [51, -3]]),
        "axes": ["x", "y", "t"],
        "axis_x_values": {"start": -3.0, "stop": 0.0, "num": 100},
        "axis_y_values": {"start": 51.0, "stop": 54.0, "num": 100},
        "axis_t_values": {"values": ["2020-08-01T12:00:00Z"]},
        "temporal_interval": "2020-08-01T12:00:00Z/2020-08-31T12:00:00Z/PT1D",
        "properties": {
            "name": "Polygon",
            "datetime": "2020-08-01T12:00:00Z/2020-08-31T12:00:00Z/PT1D",
            "detail": "http://www.example.com/define/location/61812",
            "description": "A polygon",
        },
        "referencing": [
            {"coords": ["x", "y"], "system_type": "GeographicCRS", "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "gregorian"},
        ],
    },
    "61198": {
        "geometry": Point(25, -120),
        "axes": ["t"],
        "axis_t_values": {"values": [
            "2021-01-01T00:00:00Z",
            "2021-01-01T06:00:00Z",
            "2021-01-01T12:00:00Z",
            "2021-01-01T18:00:00Z",
        ]},
        "temporal_interval": "2021-01-01T00:00:00Z/2021-02-01T00:00:00Z/PT6H",
        "properties": {
            "name": "Timeseries",
            "datetime": "2021-01-01T00:00:00Z/2021-02-01T00:00:00Z/PT6H",
            "detail": "http://www.example.com/define/location/61198",
            "description": "A point location over a timeseries",
        },
        "referencing": [
            {"coords": ["x", "y"], "system_type": "GeographicCRS", "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "gregorian"},
        ],
    },
}


LOCATIONS_LOOKUP = {
    "00001": ["50232"],
    "00002": ["50232", "61812", "61198"],
}


PARAMETERS_LOOKUP = {
    "50232": ["Parameter 1", "Parameter 3"],
    "61812": ["Parameter 2"],
    "61198": ["Parameter 1", "Parameter 3"],
}


class Locations(Locations):
    def __init__(self, collection_id, query_parameters: dict) -> None:
        super().__init__(collection_id, query_parameters)
        self._parameters = self.parameters()

    def _bbox_filter(self, location: Feature) -> bool:
        bbox_extent = self.query_parameters["bbox"]
        bbox = box(
            bbox_extent["xmin"], bbox_extent["ymin"], bbox_extent["xmax"], bbox_extent["ymax"]
        )
        geometry = LOCATIONS[location.id][0]
        return bbox.intersects(geometry)

    def _datetime_filter(self, location: Feature) -> bool:
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

    def parameters(self) -> List[Parameter]:
        params = []
        for name, metadata in PARAMETERS.items():
            param = Parameter(name, **metadata)
            params.append(param)
        return params

    def references(self, refs_list: List) -> List[Referencing]:
        refs = []
        for ref_dict in refs_list:
            ref = Referencing(**ref_dict)
            refs.append(ref)
        return refs

    def all_locations(self) -> List[Feature]:
        locs_list = []
        for loc_id, loc_metadata in LOCATIONS.items():
            geometry_type, coord_list, bbox = self._handle_geometry(loc_metadata["geometry"])
            location_parameter_names = PARAMETERS_LOOKUP[loc_id]
            loc_parameters = filter(lambda param: param.name in location_parameter_names, self._parameters)
            loc_refs = self.references(loc_metadata["referencing"])
            loc = Feature(**{
                "id": loc_id,
                "geometry_type": geometry_type,
                "coords": coord_list,
                "bbox": bbox,
                "axes": loc_metadata["axes"],
                "axis_x_values": loc_metadata.get("axis_x_values", {}),
                "axis_y_values": loc_metadata.get("axis_y_values", {}),
                "axis_z_values": loc_metadata.get("axis_z_values", {}),
                "axis_t_values": loc_metadata.get("axis_t_values", {}),
                "temporal_interval": loc_metadata["temporal_interval"],
                "properties": loc_metadata["properties"],
                "parameters": list(loc_parameters),
                "referencing": loc_refs,
            })
            locs_list.append(loc)
        return locs_list

    def get_collection_bbox(self):
        from .admin import SAMPLES
        return SAMPLES[self.collection_id][-2]


class Location(Location):
    def _tilesets(self, param_name) -> List[Tileset]:
        """Define tilesets metadata for a specific parameter."""
        free_axis = "t"
        param_metadata = PARAMETERS[param_name]
        tile_shape = [None] * len(param_metadata["axes"])
        tile_shape[param_metadata["axes"].index(free_axis)] = 1
        url_template = urljoin(self.items_url, f"items/{param_name}_{{{free_axis}}}")
        return [Tileset(tile_shape, url_template)]

    def parameters(self) -> List[Parameter]:
        selected_parameters = self._parameter_filter(PARAMETERS_LOOKUP[self.location_id])
        params = []
        for parameter_name in selected_parameters:
            metadata = PARAMETERS[parameter_name]
            param = Parameter(parameter_name, **metadata)
            if metadata["value_type"] == "tilesets":
                tilesets = self._tilesets(parameter_name)
                param.values = tilesets
            params.append(param)
        return params

    def data(self) -> Feature:
        location_parameters = self.parameters()
        locations_provider = Locations(self.collection_id, self.query_parameters)
        this_location, = list(filter(lambda l: l.id == self.location_id, locations_provider.all_locations()))
        this_location.parameters = location_parameters
        return this_location
