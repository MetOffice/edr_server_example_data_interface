import re
from typing import List, Union
from urllib.parse import urljoin

from edr_server.abstract_data_interface.items import (
    Feature, FeatureCollection, Item, Items, Parameter
)

from . import dataset
from .locations import Location, Locations


class Items(Items):
    def _get_features(self) -> List[Feature]:
        # Get features to serve as items.
        in_features = {}  # In future more EDR contents than locations (e.g. area, cube) might provide features
        locations_provider = Locations(self.collection_id, self.query_parameters)
        locations = locations_provider.locations_filter(locations_provider.all_locations())
        in_features["locations"] = locations

        # Present located features as items.
        out_features = []
        for feature_type, features in in_features.items():
            for feature in features:
                feature_href = urljoin(self.collection_href, f"{feature_type}/{feature.id}")
                out_feature = Feature(
                    feature.id,
                    feature.geometry_type,
                    feature.coords,
                    feature.properties,
                    feature_href
                )
                out_features.append(out_feature)
        return out_features

    def data(self) -> FeatureCollection:
        features = self._get_features()
        n_features = len(features)
        return FeatureCollection(
            links=[],
            number_matched=n_features,
            number_returned=n_features,
            timestamp=self._get_timestamp(),
            items=features
        )


class Item(Item):
    def _has_item(self) -> bool:
        # Check the parameter is in the collection.
        coll_locations = dataset.LOCATIONS_COLLECTIONS_LOOKUP[self.collection_id]
        coll_param_names = []
        for location in coll_locations:
            coll_param_names.extend(dataset.PARAMETERS_LOCATIONS_LOOKUP[location])
        coll_param_names = list(set(coll_param_names))
        return self.param_name in coll_param_names

    def _can_provide_data(self, parameter) -> bool:
        # Check the parameter returns a tileset.
        param_has_tilesets = parameter.value_type == "tilesets"

        # Check the axes indices are integers.
        axis_inds_are_int = all([isinstance(a, int) for a in self.axes_inds])
        return param_has_tilesets & axis_inds_are_int

    def _handle_data(self, param):
        """Locate the parameter's gridded data and subset it to the 2D tile requested."""
        param_data = dataset.DATA[param.name]
        url_template = param.values[0].url_template
        item_template = url_template.split("/")[-1]
        self.free_axes = re.findall(r"{([\w]?)}", item_template)
        slicer = [slice(None)] * len(param.shape)
        for (axis_name, idx) in zip(self.free_axes, self.axes_inds):
            slicer[param.axes.index(axis_name)] = slice(idx, idx+1)
        return param_data[tuple(slicer)]

    def _find_valid_location_id(self):
        """Find the ID of a location that contains the specified parameter."""
        for loc_id, param_names in dataset.PARAMETERS_LOCATIONS_LOOKUP.items():
            if self.param_name in param_names:
                result = loc_id
                break
        return result

    def data(self) -> Union[Parameter, None]:
        result = None
        if self._has_item():
            valid_loc_id = self._find_valid_location_id()
            parameters = Location(self.collection_id, valid_loc_id, {}, "http://dummy:8000").parameters()
            param, = list(filter(lambda p: p.name == self.param_name, parameters))
            if self._can_provide_data(param):
                try:
                    indexed_data = self._handle_data(param)
                except IndexError:
                    result = None
                else:
                    result = Parameter(
                        type=param.type,
                        dtype=param.dtype,
                        axes=param.axes,
                        shape=self._tile_shape(param),
                        values=self._prepare_data(indexed_data)
                    )
        return result