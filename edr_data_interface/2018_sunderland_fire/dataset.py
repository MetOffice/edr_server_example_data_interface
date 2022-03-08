import os
from typing import Dict, List

import iris
from shapely.geometry import Polygon


class DataProvider(object):
    def __init__(self) -> None:
        # XXX do this better in future!
        self.data_path = "/Users/dpeterk/data/3DT/2018_sunderland_fire/basic_name_run"
        self.data_name = "Fields*.txt"

        self._data = None

    @property
    def data(self):
        if self._data is None:
            self.load_data()
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def load_data(self):
        self.data = iris.load(os.path.join(self.data_path, self.data_name))

    def get_cube(self, cube_ref):
        """Locate a cube based on its reference (one of its name / 'field name' attribute)."""
        if not isinstance(cube_ref, int):
            cube_ref = -1
            for i, cube in enumerate(self.data):
                matchers = [cube.name(), cube.attributes["Field Name"]]
                if cube_ref in matchers:
                    cube_ref = i
                    break
            if cube_ref == -1:
                raise IndexError(f"Cube matching reference {cube_ref!r} could not be found.")
        return self.data[cube_ref]

    def get_axes(self, cube_ref=None) -> List:
        """
        Determine the list of named axes (from `[x, y, z, t]`) present in the specified cube.

        """
        if cube_ref is None:
            cube_ref = 0
        cube = self.get_cube(cube_ref)
        axes = ["x", "y", "z", "t"]
        result = []
        for axis in axes:
            if len(cube.coords(dim_coords=True, axis=axis)):
                result.append(axis)
        return result

    def get_bbox(self, cube_ref=None) -> List:
        """
        Get the bounding box ('bbox') of the specified cube as a list of:
            `[lon_min, lat_min, lon_max, lat_max]`

        """
        if cube_ref is None:
            cube_ref = 0
        cube = self.get_cube(cube_ref)
        lat_min = cube.coord("latitude").points[0]
        lat_max = cube.coord("latitude").points[-1]
        lon_min = cube.coord("longitude").points[0]
        lon_max = cube.coord("longitude").points[-1]
        return [lon_min, lat_min, lon_max, lat_max]

    def get_geometry(self, cube_ref=None) -> Polygon:
        """Convert `self.bbox` into a shapely Polygon instance."""
        xl, yl, xh, yh = self.get_bbox(cube_ref)
        return Polygon([[xl, yl], [xl, yh], [xh, yh], [xh, yl], [xl, yl]])

    def get_named_coord_points(self, coord_name, cube_ref=None) -> Dict:
        """
        Get the points for a named coordinate - either as the list of point values
        (if there are only a limited number of values), or as the definition for a
        linearly spaced array of points.

        """
        if cube_ref is None:
            cube_ref = 0
        cube = self.get_cube(cube_ref)
        if len(coord_name) == 1:
            coord, = cube.coords(dim_coords=True, axis=coord_name)
        else:
            coord = cube.coord(coord_name)
        coord_shape, = coord.shape
        if coord_shape < 35:
            result = {"values": coord.points}
        else:
            result = {
                "start": coord.points[0],
                "stop": coord.points[-1],
                "num": coord_shape,
            }
        return result

    def get_t_coord_values(self, cube_ref=None) -> List:
        """Get a list of time coordinate points from the specified cube as ISO8601 standard values."""
        if cube_ref is None:
            cube_ref = 0
        cube = self.get_cube(cube_ref)
        time_coord = cube.coord("time")
        time_unit = time_coord.units
        time_points = time_coord.points
        return [time_unit.num2date(p).strftime("%Y-%m-%dT%H:%M:%SZ") for p in time_points]

    def get_attributes(self, cube_ref=None) -> Dict:
        """Get the attributes dictionary of the specified cube."""
        if cube_ref is None:
            cube_ref = 0
        cube = self.get_cube(cube_ref)
        return cube.attributes


DATA_PROVIDER = DataProvider()


CATEGORY_ENCODING = {
    "#FFFFEB": 3.2e-9,
    "#F5FBD6": 1e-8,
    "#E3F3D9": 3.2e-8,
    "#BFED6C": 1e-7,
    "#A0DAE1": 3.2e-7,
    "#8DC7DF": 0.000001,
    "#90AED3": 0.0000032,
    "#9199C9": 0.00001,
    "#838DAB": 0.000032,
}


DATA = {cube.attributes["Field Name"]: cube for cube in DATA_PROVIDER.data}


CRS = (
    "GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,"
    "AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],"
    "PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],"
    "UNIT[\"degree\",0.01745329251994328,AUTHORITY[\"EPSG\",\"9122\"]],AUTHORITY[\"EPSG\",\"4326\"]]"
)


COLLECTIONS: Dict = {
    "sunderland_09082021_1900Z": {
        "name": "NAME Sunderland EDR demonstrator",
        "id": "sunderland_09082021_1900Z",
        "description": "API to access data for a release scenerio in Sunderland starting at 14/05/2018 19:00 UTC data (not for operational use)",
        "keywords": [
            "NAME",
            "Sunderland",
            "Concentration",
            "Air",
            "Wet",
            "Dry",
            "Deposition",
        ],
        "bbox": DATA_PROVIDER.get_bbox(),
        "crs": CRS,
        "crs_name": "WGS 1984",
    },
}


TEMPORAL_EXTENTS: Dict = {
    "sunderland_09082021_1900Z": {
        "temporal_interval": ["2018-05-14T20:00Z/2018-05-15T19:00Z/PT1H"],
        "temporal_values": DATA_PROVIDER.get_t_coord_values(),
        "trs": "TIMECRS[\"DateTime\",TDATUM[\"Gregorian Calendar\"],CS[TemporalDateTime,1],AXIS[\"Time (T)\",future]",
        "temporal_name": "",
    },
}


LOCATIONS = {
    "1.3987W_54.1948N_1405201819:00UTC": {
        "geometry": DATA_PROVIDER.get_geometry(),
        "axes": DATA_PROVIDER.get_axes(),
        "axis_x_values": DATA_PROVIDER.get_named_coord_points("x"),
        "axis_y_values": DATA_PROVIDER.get_named_coord_points("y"),
        "axis_t_values": {"values": TEMPORAL_EXTENTS["sunderland_09082021_1900Z"]["temporal_values"]},
        "temporal_interval": TEMPORAL_EXTENTS["sunderland_09082021_1900Z"]["temporal_interval"],
        "properties": DATA_PROVIDER.get_attributes(),
        "referencing": [
            {
                "coords": ["x", "y"],
                "system_type": "GeographicCRS",
                "system_id": "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
            },
            {
                "coords": ["t"],
                "system_type": "TemporalRS",
                "system_calendar": "Gregorian",
            },
        ],
    }
}


PARAM_EXTRAS: Dict = {
    'Unnamed Field Req 1': {
        "unit": "g/m-3",
        "unit_type": "http://labs.metoffice.gov.uk/edr/metadata/units/g/m-3",
        "phenomenon_id": "http://codes.wmo.int/grib2/codeflag/4.2/0-18-10",
    },
    'Unnamed Field Req 2': {
        "unit": "g/m-3",
        "unit_type": "http://labs.metoffice.gov.uk/edr/metadata/units/g/m-3",
        "phenomenon_id": "http://codes.wmo.int/grib2/codeflag/4.2/0-18-10",
    },
    'Unnamed Field Req 3': {
        "unit": "g/m-2",
        "unit_type": "http://labs.metoffice.gov.uk/edr/metadata/units/g/m-2",
        "phenomenon_id": "http://codes.wmo.int/grib2/codeflag/4.2/0-18-11",
    },
    'Unnamed Field Req 4': {
        "unit": "g/m-2",
        "unit_type": "http://labs.metoffice.gov.uk/edr/metadata/units/g/m-2",
        "phenomenon_id": "http://codes.wmo.int/grib2/codeflag/4.2/0-18-12",
    },
    'Unnamed Field Req 5': {
        "unit": "g/m-2",
        "unit_type": "http://labs.metoffice.gov.uk/edr/metadata/units/g/m-2",
        "phenomenon_id": "http://codes.wmo.int/grib2/codeflag/4.2/0-18-13",
    },
    'Unnamed Field Req 6': {
        "unit": "g/m-2",
        "unit_type": "http://labs.metoffice.gov.uk/edr/metadata/units/g/m-2",
        "phenomenon_id": "http://codes.wmo.int/grib2/codeflag/4.2/0-18-10",
    },
}


# XXX effectively swapping ID and name here as there are cubes with duplicate names.
PARAMETERS: Dict = {}
for name, cube in DATA.items():
    param = {
        "id": cube.name(),
        "description": f"{name} - {cube.name().lower().replace('_', ' ')}",
        "type": "TiledNdArray",
        "dtype": cube.dtype.name,
        "axes": ["t", "y", "x"],
        "shape": cube.shape,
        "value_type": "tilesets",
        "values": [],
        "unit": PARAM_EXTRAS[name]["unit"],
        "unit_label": cube.units,
        "unit_type": PARAM_EXTRAS[name]["unit_type"],
        "phenomenon_id": PARAM_EXTRAS[name]["phenomenon_id"],
        "phenomenon": cube.name(),
        "category_encoding": CATEGORY_ENCODING,
    }
    # Cell methods are stored in this awkwardly-named cube attribute...
    t_averaging = DATA_PROVIDER.get_attributes().get("Time av/int info")
    if t_averaging is not None:
        h, _, statistic = t_averaging.split(" ")
        param.update({
            "measurement_type_method": statistic,
            "measurement_type_period": f"PT{h[:-1].upper()}",
        })
    PARAMETERS[name] = param


PARAMETERS_COLLECTIONS_LOOKUP = {
    "sunderland_09082021_1900Z": list(PARAMETERS.keys()),
}


LOCATIONS_COLLECTIONS_LOOKUP = {
    "sunderland_09082021_1900Z": list(LOCATIONS.keys()),
}


PARAMETERS_LOCATIONS_LOOKUP = {
    list(LOCATIONS.keys())[0]: list(PARAMETERS.keys()),
}