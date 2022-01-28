from .core import Interface


class RefreshCollections(Interface):
    def __init__(self, supported_data_queries) -> None:
        self.supported_data_queries = supported_data_queries
        self.temporal_extent = False
        self.vertical_extent = False

        self._get_temporal_extent()
        self._get_vertical_extent()

    def _get_temporal_extent(self):
        """
        Determine if the collection's data has a temporal extent.

        Must set `self.temporal_extent`, and also determine `interval`, `trs` and `name`
        for the temporal extent JSON response. The `trs` variable must be provided
        as well-known text (WKT).
        
        """
        self.temporal_extent = False

    def _get_vertical_extent(self):
        """
        Determine if the collection's data has a vertical extent.

        Must set `self.vertical_extent`, and also determine `interval`, `vrs` and `name`
        for the vertical extent JSON response. The `vrs` variable must be provided
        as well-known text (WKT).
        
        """
        self.vertical_extent = False

    def has_temporal_extent(self):
        """Define if the collection has a temporal extent."""
        return self.temporal_extent

    def has_vertical_extent(self):
        """Define if the collection has a vertical extent."""
        return self.vertical_extent

    def make_collection(self, name):
        raise NotImplemented

    def make_collections(self):
        raise NotImplemented

    def data(self):
        return self.make_collections()