from typing import Dict

import numpy as np
from shapely.geometry import Point, Polygon


def construct_data_3d(xy, t):
    x = y = np.arange(xy)
    t = np.arange(t)
    tm, ym, xm = np.meshgrid(t, y, x)
    levels = np.sin(0.5*xm + tm) + np.cos(0.2*ym + 2)
    return levels.transpose(1, 0, 2)  # For whatever reason the dims order isn't (t, y, x).


def construct_data_4d(xy, t, z):
    x = y = np.arange(xy, dtype="float")
    t = np.arange(t)
    z = np.arange(1, z+1)
    tm, zm, ym, xm = np.meshgrid(t, z, y, x)
    return np.sin(0.1 * zm * xm * ym + tm)


CATEGORY_ENCODING = {
    "#000": 0.0,
    "#444": 20.0,
    "#888": 40.0,
    "#ccc": 60.0,
    "#fff": 80.0,
}


DATA = {
    "Parameter 1": construct_data_3d(100, 4),
    "Parameter 2": construct_data_3d(100, 4),
    "Parameter 3": construct_data_3d(100, 4),
    "Parameter 4": construct_data_4d(25, 31, 9),
    "Parameter 5": construct_data_4d(25, 31, 9),
    "Parameter 6": np.sin(np.arange(24, dtype="float") * 0.25 - 15),
}


CRS = (
    "GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,"
    "AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],"
    "PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],"
    "UNIT[\"degree\",0.01745329251994328,AUTHORITY[\"EPSG\",\"9122\"]],AUTHORITY[\"EPSG\",\"4326\"]]"
)


COLLECTIONS: Dict = {
    "00001": {
        "name": "One",
        "id": "00001",
        "description": "The first collection",
        "keywords": ["Example", "Dummy"],
        "bbox": [-180, -90, 180, 90],
        "crs": CRS,
        "crs_name": "WGS 1984",
    },
    "00002": {
        "name": "Two",
        "id": "00002",
        "description": "The second collection",
        "keywords": ["Example", "Dummy"],
        "bbox": [-180, -90, 180, 90],
        "crs": CRS,
        "crs_name": "EPSG4326",
    },
    "00003": {
        "name": "Three",
        "id": "00003",
        "description": "The third collection",
        "keywords": ["Example", "Dummy"],
        "bbox": [55.4, -3.1, 55.6, -2.9],
        "crs": CRS,
        "crs_name": "WGS 1984",
    },
}


TEMPORAL_EXTENTS: Dict = {
    "00001": {
        "temporal_interval": ["2021-01-01T00:00:00Z/2021-02-01T00:00:00Z/PT6H"],
        "temporal_values": [
            "2021-01-01T00:00:00Z",
            "2021-01-01T06:00:00Z",
            "2021-01-01T12:00:00Z",
            "2021-01-01T18:00:00Z",
        ],
        "trs": "TIMECRS[\"DateTime\",TDATUM[\"Gregorian Calendar\"],CS[TemporalDateTime,1],AXIS[\"Time (T)\",future]",
        "temporal_name": "Dummy temporal extent",
    },
    "00002": {
        "temporal_interval": ["2020-08-01T12:00:00Z/2020-08-31T12:00:00Z/PT1D"],
        "temporal_values": [
            "2020-08-01T12:00:00Z",
            "2020-08-02T12:00:00Z",
            "2020-08-03T12:00:00Z",
            "2020-08-04T12:00:00Z",
            "2020-08-05T12:00:00Z",
            "2020-08-06T12:00:00Z",
            "2020-08-07T12:00:00Z",
            "2020-08-08T12:00:00Z",
            "2020-08-09T12:00:00Z",
            "2020-08-10T12:00:00Z",
            "2020-08-11T12:00:00Z",
            "2020-08-12T12:00:00Z",
            "2020-08-13T12:00:00Z",
            "2020-08-14T12:00:00Z",
            "2020-08-15T12:00:00Z",
            "2020-08-16T12:00:00Z",
            "2020-08-17T12:00:00Z",
            "2020-08-18T12:00:00Z",
            "2020-08-19T12:00:00Z",
            "2020-08-20T12:00:00Z",
            "2020-08-21T12:00:00Z",
            "2020-08-22T12:00:00Z",
            "2020-08-23T12:00:00Z",
            "2020-08-24T12:00:00Z",
            "2020-08-25T12:00:00Z",
            "2020-08-26T12:00:00Z",
            "2020-08-27T12:00:00Z",
            "2020-08-28T12:00:00Z",
            "2020-08-29T12:00:00Z",
            "2020-08-30T12:00:00Z",
            "2020-08-31T12:00:00Z",
        ],
        "trs": "TIMECRS[\"DateTime\",TDATUM[\"Gregorian Calendar\"],CS[TemporalDateTime,1],AXIS[\"Time (T)\",future]",
        "temporal_name": "Dummy temporal extent",
    },
    "00003": {
        "temporal_interval": ["2021-06-30T00:00:00Z/2021-07-01T00:00:00Z/PT1H"],
        "temporal_values": [
            "2021-06-30T00:00:00Z",
            "2021-06-30T01:00:00Z",
            "2021-06-30T02:00:00Z",
            "2021-06-30T03:00:00Z",
            "2021-06-30T04:00:00Z",
            "2021-06-30T05:00:00Z",
            "2021-06-30T06:00:00Z",
            "2021-06-30T07:00:00Z",
            "2021-06-30T08:00:00Z",
            "2021-06-30T09:00:00Z",
            "2021-06-30T10:00:00Z",
            "2021-06-30T11:00:00Z",
            "2021-06-30T12:00:00Z",
            "2021-06-30T13:00:00Z",
            "2021-06-30T14:00:00Z",
            "2021-06-30T15:00:00Z",
            "2021-06-30T16:00:00Z",
            "2021-06-30T17:00:00Z",
            "2021-06-30T18:00:00Z",
            "2021-06-30T19:00:00Z",
            "2021-06-30T20:00:00Z",
            "2021-06-30T21:00:00Z",
            "2021-06-30T22:00:00Z",
            "2021-06-30T23:00:00Z",
        ],
        "trs": "TIMECRS[\"DateTime\",TDATUM[\"Gregorian Calendar\"],CS[TemporalDateTime,1],AXIS[\"Time (T)\",future]",
        "temporal_name": "Dummy temporal extent",
    },
}


VERTICAL_EXTENTS: Dict = {
    "00001": {
        "vertical_interval": [],
        "vertical_values": [],
        "vrs": "VERTCS",
        "vertical_name": "Empty dummy vertical extent"
    },
    "00002": {
        "vertical_interval": ["2", "10"],
        "vertical_values": ["2", "3", "4", "5", "6", "7", "8", "9", "10"],
        "vrs": "VERTCS",
        "vertical_name": "Dummy vertical extent",
    },
    "00003": {
        "vertical_interval": [],
        "vertical_values": [],
        "vrs": "VERTCS",
        "vertical_name": "Empty dummy vertical extent"
    },
}


PARAMETERS: Dict = {
    "Parameter 1": {
        "id": "param1",
        "description": "The first dummy parameter",
        "type": "TiledNdArray",
        "dtype": DATA["Parameter 1"].dtype.name,
        "axes": ["t", "y", "x"],
        "shape": [4, 100, 100],
        "value_type": "tilesets",
        "values": [],
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
        "shape": [4, 100, 100],
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
        "type": "TiledNdArray",
        "dtype": DATA["Parameter 3"].dtype.name,
        "axes": ["t", "y", "x"],
        "shape": [4, 100, 100],
        "value_type": "tilesets",
        "values": [],
        "unit": "m s-1",
        "unit_label": "m/s",
        "unit_type": "http://www.example.com/define/unit/ms-1",
        "phenomenon_id": "http://www.example.com/phenom/dummy_3",
        "phenomenon": "Dummy 3",
        "measurement_type_method": "average",
        "measurement_type_period": "PT6H",
        "category_encoding": CATEGORY_ENCODING,
    },
    "Parameter 4": {
        "id": "param4",
        "description": "The fourth dummy parameter",
        "type": "TiledNdArray",
        "dtype": DATA["Parameter 4"].dtype.name,
        "axes": ["t", "z", "y", "x"],
        "shape": [31, 9, 25, 25],
        "value_type": "tilesets",
        "values": [],
        "unit": "K",
        "unit_label": "K",
        "unit_type": "http://www.example.com/define/unit/K",
        "phenomenon_id": "http://www.example.com/phenom/dummy_4",
        "phenomenon": "Dummy 4",
    },
    "Parameter 5": {
        "id": "param5",
        "description": "The fifth dummy parameter",
        "type": "TiledNdArray",
        "dtype": DATA["Parameter 5"].dtype.name,
        "axes": ["t", "z", "y", "x"],
        "shape": [31, 9, 25, 25],
        "value_type": "tilesets",
        "values": [],
        "unit": "%",
        "unit_label": "%RH",
        "unit_type": "http://www.example.com/define/unit/percent",
        "phenomenon_id": "http://www.example.com/phenom/dummy_5",
        "phenomenon": "Dummy 5",
        "measurement_type_method": "average",
        "measurement_type_period": "PT6H",
    },
    "Parameter 6": {
        "id": "param6",
        "description": "The sixth dummy parameter",
        "type": "NdArray",
        "dtype": DATA["Parameter 6"].dtype.name,
        "axes": ["t"],
        "shape": [24],
        "value_type": "values",
        "values": list(DATA["Parameter 6"]),
        "unit": "K",
        "unit_label": "K",
        "unit_type": "http://www.example.com/define/unit/K",
        "phenomenon_id": "http://www.example.com/phenom/dummy_6",
        "phenomenon": "Dummy 6",
    },
}


PARAMETERS_COLLECTIONS_LOOKUP = {
    "00001": ["Parameter 1", "Parameter 2", "Parameter 3"],
    "00002": ["Parameter 4", "Parameter 5"],
    "00003": ["Parameter 6"]
}


LOCATIONS_COLLECTIONS_LOOKUP = {
    "00001": ["50232"],
    "00002": ["61812", "61198"],
    "00003": ["25364"],
}


PARAMETERS_LOCATIONS_LOOKUP = {
    "50232": [
        "Parameter 1",
        "Parameter 2",
        "Parameter 3",
    ],
    "61812": ["Parameter 4"],
    "61198": ["Parameter 4", "Parameter 5"],
    "25364": ["Parameter 6"],
}


LOCATIONS = {
    "50232": {
        "geometry": Polygon([[-3, 51], [0, 51], [0, 54], [-3, 54], [-3, 51]]),
        "axes": ["x", "y", "t"],
        "axis_x_values": {"start": -3.0, "stop": 0.0, "num": 100},
        "axis_y_values": {"start": 51.0, "stop": 54.0, "num": 100},
        "axis_t_values": {"values": TEMPORAL_EXTENTS["00001"]["temporal_values"]},
        "temporal_interval": TEMPORAL_EXTENTS["00001"]["temporal_interval"],
        "properties": {
            "name": "Location 50232",
            "datetime": TEMPORAL_EXTENTS["00001"]["temporal_interval"][0],
            "detail": "http://www.example.com/define/location/50232",
            "description": "A location",
        },
        "referencing": [
            {"coords": ["x", "y"], "system_type": "GeographicCRS", "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "standard"},
        ],
    },
    "61812": {
        "geometry": Polygon([[-8, 55], [-6, 55], [-6, 57], [-8, 57], [-8, 55]]),
        "axes": ["x", "y", "t", "z"],
        "axis_x_values": {"start": -8.0, "stop": -6.0, "num": 25},
        "axis_y_values": {"start": 55.0, "stop": 57.0, "num": 25},
        "axis_t_values": {"values": TEMPORAL_EXTENTS["00002"]["temporal_values"]},
        "axis_z_values": {"values": VERTICAL_EXTENTS["00002"]["vertical_values"]},
        "temporal_interval": TEMPORAL_EXTENTS["00002"]["temporal_interval"],
        "vertical_interval": VERTICAL_EXTENTS["00002"]["vertical_interval"],
        "properties": {
            "name": "Location 61812",
            "datetime": TEMPORAL_EXTENTS["00002"]["temporal_interval"][0],
            "detail": "http://www.example.com/define/location/61812",
            "description": "A classic polygon",
        },
        "referencing": [
            {"coords": ["x", "y"], "system_type": "GeographicCRS", "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "gregorian"},
            {"coords": ["z"], "system_type": "VerticalRS", "system_id": "http://www.example.com/define/crs/vert_rs"},
        ],
    },
    "61198": {
        "geometry": Polygon([[-8, 55], [-6, 55], [-6, 57], [-8, 57], [-8, 55]]),
        "axes": ["x", "y", "t", "z"],
        "axis_x_values": {"start": -8.0, "stop": -6.0, "num": 25},
        "axis_y_values": {"start": 55.0, "stop": 57.0, "num": 25},
        "axis_t_values": {"values": TEMPORAL_EXTENTS["00002"]["temporal_values"]},
        "axis_z_values": {"values": VERTICAL_EXTENTS["00002"]["vertical_values"]},
        "temporal_interval": TEMPORAL_EXTENTS["00002"]["temporal_interval"],
        "vertical_interval": VERTICAL_EXTENTS["00002"]["vertical_interval"],
        "properties": {
            "name": "Location 61198",
            "datetime": TEMPORAL_EXTENTS["00002"]["temporal_interval"][0],
            "detail": "http://www.example.com/define/location/61198",
            "description": "A point location over a timeseries",
        },
        "referencing": [
            {"coords": ["x", "y"], "system_type": "GeographicCRS", "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "gregorian"},
            {"coords": ["z"], "system_type": "VerticalRS", "system_id": "http://www.example.com/define/crs/vert_rs"},
        ],
    },
    "25364": {
        "geometry": Point(55.5, -3.0),
        "axes": ["x", "y", "t"],
        "axis_x_values": {"values": [-3.0]},
        "axis_y_values": {"values": [55.5]},
        "axis_t_values": {"values": TEMPORAL_EXTENTS["00003"]["temporal_values"]},
        "temporal_interval": TEMPORAL_EXTENTS["00003"]["temporal_interval"],
        "properties": {
            "name": "Timeseries location 25364",
            "datetime": TEMPORAL_EXTENTS["00003"]["temporal_interval"][0],
            "detail": "http://www.example.com/define/location/25364",
            "description": "A point location over a timeseries",
        },
        "referencing": [
            {"coords": ["x", "y"], "system_type": "GeographicCRS", "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "standard"},
        ],
    }
}