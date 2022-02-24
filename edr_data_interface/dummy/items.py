from typing import List
from urllib.parse import urljoin

from edr_server.abstract_data_interface.items import (
    Feature, FeatureCollection, Items, Parameter
)

from .locations import Locations


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
                feature_href = urljoin(self.collection_href, feature_type, feature.id)
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