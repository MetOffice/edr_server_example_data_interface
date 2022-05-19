from typing import List, Tuple, Union
from urllib.parse import urljoin

from edr_server.abstract_data_interface.locations import Feature, Location, Locations, Parameter, Referencing, Tileset
from shapely.geometry import box

from . import dataset


class Parameters(object):
    """Handle construction of data-providing parameters."""
    def __init__(self, selected_parameters: List, item_url: str) -> None:
        self.selected_parameters = selected_parameters
        self.item_url = item_url

    def _tilesets(self, param_name) -> List[Tileset]:
        """Define tilesets metadata for a specific parameter."""
        param_metadata = dataset.PARAMETERS[param_name][0]
        free_axes = list(set(param_metadata["axes"]) - {"x", "y"})
        tile_shape = [None] * len(param_metadata["axes"])
        url_extension = ""
        for free_axis in free_axes:
            tile_shape[param_metadata["axes"].index(free_axis)] = 1
            url_extension += f"_{{{free_axis}}}"
        url_template = urljoin(self.item_url, f"items/{param_name}{url_extension}")
        return [Tileset(tile_shape, url_template)]

    def _values(self, param_name):
        return dataset.DATA[param_name]

    def parameters(self) -> List[Parameter]:
        params = []
        for parameter_name in self.selected_parameters:
            metadata = dataset.PARAMETERS[parameter_name]
            param = Parameter(parameter_name, **metadata[0])
            if metadata[0]["value_type"] == "tilesets":
                tilesets = self._tilesets(parameter_name)
                param.values = tilesets
            elif metadata[0]["value_type"] == "values":
                param.values = self._values(parameter_name)
            params.append(param)
        return params


class Locations(Locations):
    def __init__(self, collection_id, query_parameters: dict) -> None:
        super().__init__(collection_id, query_parameters)
        self._parameters = self.parameters()

    def _bbox_filter(self, location: Feature) -> bool:
        bbox_extent = self.query_parameters["bbox"]
        bbox = box(
            bbox_extent["xmin"], bbox_extent["ymin"], bbox_extent["xmax"], bbox_extent["ymax"]
        )
        geometry = dataset.LOCATIONS[location.id].geometry
        return bbox.intersects(geometry)

    def _datetime_filter(self, location: Feature) -> bool:
        return True

    def locations_filter(self, locations):
        """Filter locations by collection ID and any request query parameters."""
        collection_location_ids = dataset.LOCATIONS_COLLECTIONS_LOOKUP[self.collection_id]
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
        for name, metadata in dataset.PARAMETERS.items():
            param = Parameter(name, **metadata[0])
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
        for loc_id, loc_metadata in dataset.LOCATIONS.items():
            geometry_type, coord_list, bbox = self._handle_geometry(loc_metadata["geometry"])
            location_parameter_names = dataset.PARAMETERS_LOCATIONS_LOOKUP[loc_id]
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
        from .dataset import COLLECTIONS
        return COLLECTIONS[self.collection_id].extent.spatial.bbox.bounds


class Location(Location):
    def _check_location(self) -> bool:
        return self.location_id in dataset.LOCATIONS.keys()

    def parameters(self) -> List[Parameter]:
        selected_parameters = self._parameter_filter(dataset.PARAMETERS_LOCATIONS_LOOKUP[self.location_id])
        parameter_provider = Parameters(selected_parameters, self.items_url)
        return parameter_provider.parameters()

    def data(self) -> Tuple[Union[Feature, None], Union[str, None]]:
        error = None
        if not self._check_location():
            this_location = None
            error = "No such location"
        else:
            location_parameters = self.parameters()
            if not len(location_parameters):
                this_location = None
                error = "No matching parameters"
            else:
                locations_provider = Locations(self.collection_id, self.query_parameters)
                filtered_locations = locations_provider.locations_filter(locations_provider.all_locations())
                try:
                    # Look for the requested location in the filtered list of locations.
                    this_location, = list(filter(lambda l: l.id == self.location_id, filtered_locations))
                    this_location = self._datetime_filter(this_location)
                    this_location = self._z_filter(this_location)
                except ValueError:
                    # Handle the location not being found.
                    this_location = None
                    error = "Location not found"
                else:
                    this_location.parameters = location_parameters
        return this_location, error
