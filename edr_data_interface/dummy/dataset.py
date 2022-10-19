import numpy as np
from datetime import datetime, timedelta, timezone
from shapely.geometry import Point, Polygon, box
from typing import Any, Dict, List, Optional, Tuple

from edr_server.core.models import EdrDataQuery
from edr_server.core.models.extents import Extents, SpatialExtent, TemporalExtent, VerticalExtent
from edr_server.core.models.metadata import CollectionMetadata
from edr_server.core.models.parameters import ObservedProperty, Parameter, Symbol, Unit
from edr_server.core.models.urls import URL, EdrUrlResolver


def construct_data_3d(xy, t):
    x = y = np.arange(xy)
    t = np.arange(t)
    tm, ym, xm = np.meshgrid(t, y, x)
    levels = np.sin(0.5 * xm + tm) + np.cos(0.2 * ym + 2)
    return levels.transpose(1, 0, 2)  # For whatever reason the dims order isn't (t, y, x).


def construct_data_4d(xy, t, z):
    x = y = np.arange(xy, dtype="float")
    t = np.arange(t)
    z = np.arange(1, z + 1)
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
    "param1": construct_data_3d(100, 4),
    "param2": construct_data_3d(100, 4),
    "param3": construct_data_3d(100, 4),
    "param4": construct_data_4d(25, 31, 9),
    "param5": construct_data_4d(25, 31, 9),
    "param6": np.sin(np.arange(24, dtype="float") * 0.25 - 15),
    "param7": np.sin(np.arange(24, dtype="float") * 0.25 - 15),
    "param8": np.sin(np.arange(24, dtype="float") * 0.25 - 15),
    "param9": np.sin(np.arange(24, dtype="float") * 0.25 - 15),
    "param10": np.sin(np.arange(24, dtype="float") * 0.25 - 15),
}

PARAMETERS: Dict[str, Tuple[Dict[str, Any], Optional[Parameter]]] = {
    param_tuple[1].id: param_tuple for param_tuple in [
        (
            {
                "id": "param1",
                "description": "The first dummy parameter",
                "type": "TiledNdArray",
                "dtype": DATA["param1"].dtype.name,
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
            Parameter(
                id="param1",
                label="Parameter 1",
                description="The first dummy parameter",
                unit=Unit("meters per second", Symbol("m/s")),
                observed_property=ObservedProperty("Airspeed velocity of an unladen swallow (European)"),
                data_type=DATA["param1"].dtype.type,
            )
        ),
        (
            {
                "id": "param2",
                "description": "The second dummy parameter",
                "type": "TiledNdArray",
                "dtype": DATA["param2"].dtype.name,
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
            Parameter(
                id="param2",
                label="Parameter 2",
                description="The second dummy parameter",
                unit=Unit("Kelvin", Symbol("K")),
                observed_property=ObservedProperty("Body temperature of an unladen swallow (European)"),
                data_type=DATA["param2"].dtype.type,
            )
        ),
        (
            {
                "id": "param3",
                "description": "The third dummy parameter",
                "type": "TiledNdArray",
                "dtype": DATA["param3"].dtype.name,
                "axes": ["t", "y", "x"],
                "shape": [4, 100, 100],
                "value_type": "tilesets",
                "values": [],
                "unit": "m s-1",
                "unit_label": "m/s",
                "unit_type": "http://www.example.com/define/unit/ms-1",
                "phenomenon_id": "http://www.example.com/phenom/dummy_1",
                "phenomenon": "Dummy 1",
                "measurement_type_method": "average",
                "measurement_type_period": "PT6H",
                "category_encoding": CATEGORY_ENCODING,
            },
            Parameter(
                id="param3",
                label="Parameter 3",
                description="The third dummy parameter",
                unit=Unit("meters per second", Symbol("m/s")),
                observed_property=ObservedProperty("Airspeed velocity of an unladen swallow (African)"),
                data_type=DATA["param3"].dtype.type,
            )
        ),
        (
            {
                "id": "param4",
                "description": "The fourth dummy parameter",
                "type": "TiledNdArray",
                "dtype": DATA["param4"].dtype.name,
                "axes": ["t", "z", "y", "x"],
                "shape": [31, 9, 25, 25],
                "value_type": "tilesets",
                "values": [],
                "unit": "K",
                "unit_label": "K",
                "unit_type": "http://www.example.com/define/unit/K",
                "phenomenon_id": "http://www.example.com/phenom/dummy_2",
                "phenomenon": "Dummy 2",
            },
            Parameter(
                id="param4",
                label="Parameter 4",
                description="The fourth dummy parameter",
                unit=Unit("Kelvin", Symbol("K")),
                observed_property=ObservedProperty("Body temperature of an unladen swallow (African)"),
                data_type=DATA["param4"].dtype.type,
            )
        ),
        (
            {
                "id": "param5",
                "description": "The fifth dummy parameter",
                "type": "TiledNdArray",
                "dtype": DATA["param5"].dtype.name,
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
            Parameter(
                id="param5",
                label="Parameter 5",
                description="The fifth dummy parameter",
                unit=Unit("%RH", Symbol("%")),
                observed_property=ObservedProperty("Relative Humidity"),
                data_type=DATA["param5"].dtype.type,
            )
        ),
        (
            {
                "id": "param6",
                "description": "The sixth dummy parameter",
                "type": "NdArray",
                "dtype": DATA["param6"].dtype.name,
                "axes": ["t"],
                "shape": [24],
                "value_type": "values",
                "values": list(DATA["param6"]),
                "unit": "K",
                "unit_label": "K",
                "unit_type": "http://www.example.com/define/unit/K",
                "phenomenon_id": "http://www.example.com/phenom/dummy_2",
                "phenomenon": "Dummy 2",
            },
            Parameter(
                id="param6",
                label="Parameter 6",
                description="The sixth dummy parameter",
                unit=Unit("Kelvin", Symbol("K")),
                observed_property=ObservedProperty("Body temperature of a Norwegian Blue parrot (Deceased)"),
                data_type=DATA["param6"].dtype.type,
            )
        ),
        (
            {
                "id": "param7",
                "description": "The seventh dummy parameter",
                "type": "NdArray",
                "dtype": DATA["param7"].dtype.name,
                "axes": ["t", "z"],
                "shape": [31, 2],
                "value_type": "values",
                "values": [],
                "unit": "K",
                "unit_label": "K",
                "unit_type": "http://www.example.com/define/unit/K",
                "phenomenon_id": "http://www.example.com/phenom/dummy_2",
                "phenomenon": "Dummy 2",
            },
            Parameter(
                id="param7",
                label="Parameter 7",
                description="The seventh dummy parameter",
                unit=Unit("Kelvin", Symbol("K")),
                observed_property=ObservedProperty("Body temperature of a Norwegian Blue parrot (Sleeping)"),
                data_type=DATA["param7"].dtype.type,
            )
        ),
        (
            {
                "id": "param8",
                "description": "The eighth dummy parameter",
                "type": "NdArray",
                "dtype": DATA["param8"].dtype.name,
                "axes": ["t", "z"],
                "shape": [31, 2],
                "value_type": "values",
                "values": [],
                "unit": "%",
                "unit_label": "%RH",
                "unit_type": "http://www.example.com/define/unit/percent",
                "phenomenon_id": "http://www.example.com/phenom/dummy_5",
                "phenomenon": "Dummy 5",
            },
            Parameter(
                id="param8",
                label="Parameter 8",
                description="The eighth dummy parameter",
                unit=Unit("%RH", Symbol("%")),
                observed_property=ObservedProperty("Relative Humidity of a Norwegian Blue parrot in a stuffy room"),
                data_type=DATA["param8"].dtype.type,
            )
        ),
        (
            {
                "id": "param9",
                "description": "The ninth dummy parameter",
                "type": "NdArray",
                "dtype": DATA["param9"].dtype.name,
                "axes": ["t"],
                "shape": [31],
                "value_type": "values",
                "values": [],
                "unit": "m s-1",
                "unit_label": "m/s",
                "unit_type": "http://www.example.com/define/unit/ms-1",
                "phenomenon_id": "http://www.example.com/phenom/dummy_1",
                "phenomenon": "Dummy 1",
            },
            Parameter(
                id="param9",
                label="Parameter 9",
                description="The ninth dummy parameter",
                unit=Unit("meters per second", Symbol("m/s")),
                observed_property=ObservedProperty("Wind Speed"),
                data_type=DATA["param9"].dtype.type,
            )
        ),
        (
            {
                "id": "param10",
                "description": "The seventh dummy parameter",
                "type": "NdArray",
                "dtype": DATA["param10"].dtype.name,
                "axes": ["t"],
                "shape": [31],
                "value_type": "values",
                "values": [],
                "unit": "deg",
                "unit_label": "deg",
                "unit_type": "http://www.example.com/define/unit/degrees",
                "phenomenon_id": "http://www.example.com/phenom/dummy_10",
                "phenomenon": "Dummy 10",
            },
            Parameter(
                id="param10",
                label="Parameter 10",
                description="The tenth dummy parameter",
                unit=Unit("Degrees Celsius", Symbol("Cel")),
                observed_property=ObservedProperty("Temperature"),
                data_type=DATA["param10"].dtype.type,
            )
        ),
    ]
}

PARAMETERS_COLLECTIONS_LOOKUP: Dict[str, List[str]] = {
    "00001": ["param1", "param2", "param3"],
    "00002": ["param4", "param5"],
    "00003": ["param6"],
    "00004": ["param7", "param8"],  # 2m and 10m
    "00005": ["param9", "param10"],  # 10m only
}

COLLECTIONS: Dict[str, CollectionMetadata] = {
    "00001": CollectionMetadata(
        title="One",
        id="00001",
        description="The first collection",
        keywords=["Example", "Dummy"],
        extent=Extents(
            spatial=SpatialExtent(box(-180, -90, 180, 90)),
            temporal=TemporalExtent(
                values=[
                    datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                    datetime(2021, 1, 1, 6, 0, 0, tzinfo=timezone.utc),
                    datetime(2021, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
                    datetime(2021, 1, 1, 18, 0, 0, tzinfo=timezone.utc),
                ]
            ),
            vertical=None
        ),
        data_queries=CollectionMetadata.get_data_query_links(
            EdrUrlResolver(URL("https://example.com")), "00001", [query for query in EdrDataQuery]),
        output_formats=["application/prs.coverage+json"],
        parameters=[PARAMETERS[param_id][1] for param_id in PARAMETERS_COLLECTIONS_LOOKUP["00001"]],
    ),
    "00002": CollectionMetadata(
        title="Two",
        id="00002",
        description="The second collection",
        keywords=["Example", "Dummy"],
        extent=Extents(
            spatial=SpatialExtent(box(-180, -90, 180, 90)),
            temporal=TemporalExtent(
                values=[
                    datetime(2020, 8, 1, 12, 0, 0, tzinfo=timezone.utc) + timedelta(days=days) for days in range(32)
                ]
            ),
            vertical=VerticalExtent([2, 3, 4, 5, 6, 7, 8, 9, 10])
        ),
        data_queries=CollectionMetadata.get_data_query_links(
            EdrUrlResolver(URL("https://example.com")), "00002", [query for query in EdrDataQuery]),
        output_formats=["application/prs.coverage+json"],
        parameters=[PARAMETERS[param_id][1] for param_id in PARAMETERS_COLLECTIONS_LOOKUP["00002"]],
    ),
    "00003": CollectionMetadata(
        title="Three",
        id="00003",
        description="The third collection",
        keywords=["Example", "Dummy"],
        extent=Extents(
            spatial=SpatialExtent(box(55.4, -3.1, 55.6, -2.9)),
            temporal=TemporalExtent(
                values=[
                    datetime(2021, 6, 30, 0, 0, 0, tzinfo=timezone.utc) + timedelta(hours=hours) for hours in range(24)
                ]
            ),
            vertical=None
        ),
        data_queries=CollectionMetadata.get_data_query_links(
            EdrUrlResolver(URL("https://example.com")), "00003", [query for query in EdrDataQuery]),
        output_formats=["application/prs.coverage+json"],
        parameters=[PARAMETERS[param_id][1] for param_id in PARAMETERS_COLLECTIONS_LOOKUP["00003"]],
    ),
    "00004": CollectionMetadata(
        title="Four",
        id="00004",
        description="The fourth collection",
        keywords=["Example", "Dummy"],
        extent=Extents(
            spatial=SpatialExtent(box(50.4, -4.0, 55.5, 1.6)),
            temporal=TemporalExtent(
                values=[
                    datetime(2020, 8, 1, 12, 0, 0, tzinfo=timezone.utc) + timedelta(days=days) for days in range(32)
                ]
            ),
            vertical=VerticalExtent([2, 10])
        ),
        data_queries=CollectionMetadata.get_data_query_links(
            EdrUrlResolver(URL("https://example.com")), "00004", [query for query in EdrDataQuery]),
        output_formats=["application/prs.coverage+json"],
        parameters=[PARAMETERS[param_id][1] for param_id in PARAMETERS_COLLECTIONS_LOOKUP["00004"]],

    ),
    "00005": CollectionMetadata(
        title="Five",
        id="00005",
        description="The fifth collection",
        keywords=["Example", "Dummy"],
        extent=Extents(
            spatial=SpatialExtent(box(50.4, -4.0, 55.5, 1.6)),
            temporal=TemporalExtent(
                values=[
                    datetime(2020, 8, 1, 12, 0, 0, tzinfo=timezone.utc) + timedelta(days=days) for days in range(32)
                ]
            ),
            vertical=VerticalExtent([2])
        ),
        data_queries=CollectionMetadata.get_data_query_links(
            EdrUrlResolver(URL("https://example.com")), "00005", [query for query in EdrDataQuery]),
        output_formats=["application/prs.coverage+json"],
        parameters=[PARAMETERS[param_id][1] for param_id in PARAMETERS_COLLECTIONS_LOOKUP["00005"]],
    ),
}

TEMPORAL_EXTENTS: Dict[str, Dict[str, Any]] = {
    collection_id: {
        "temporal_interval": [COLLECTIONS[collection_id].extent.temporal.bounds],
        "temporal_values": [dt.isoformat() for dt in COLLECTIONS[collection_id].extent.temporal.values],
        "trs": str(COLLECTIONS[collection_id].extent.temporal.trs),
        "temporal_name": COLLECTIONS[collection_id].extent.temporal.trs.name,
    }
    for collection_id in COLLECTIONS
}

VERTICAL_EXTENTS: Dict[str, Dict[str, Any]] = {
    collection_id: {
        "vertical_interval": list(map(str, COLLECTIONS[collection_id].extent.vertical.bounds)),
        "vertical_values": list(map(str, COLLECTIONS[collection_id].extent.vertical.values)),
        "vrs": str(COLLECTIONS[collection_id].extent.vertical.vrs),
        "vertical_name": COLLECTIONS[collection_id].extent.vertical.vrs.name
    }
    for collection_id in COLLECTIONS
    if COLLECTIONS[collection_id].extent.vertical
}

LOCATIONS_COLLECTIONS_LOOKUP: Dict[str, List[str]] = {
    "00001": ["50232"],
    "00002": ["61812", "61198"],
    "00003": ["25364"],
    "00004": [
        "mast1", "mast2", "mast3", "mast4", "mast5", "mast6", "mast7", "mast8", "mast9", "mast10", "mast11", "mast12"
    ],
    "00005": [
        "mast1", "mast2", "mast3", "mast4", "mast5", "mast6", "mast7", "mast8", "mast9", "mast10", "mast11", "mast12"
    ],
}

PARAMETERS_LOCATIONS_LOOKUP: Dict[str, List[str]] = {
    "50232": ["param1", "param2", "param3"],
    "61812": ["param4"],
    "61198": ["param4", "param5"],
    "25364": ["param6"],
    "mast1": ["param7", "param8", "param9", "param10"],
    "mast2": ["param7", "param8", "param9", "param10"],
    "mast3": ["param7", "param8", "param9", "param10"],
    "mast4": ["param7", "param8", "param9", "param10"],
    "mast5": ["param7", "param8", "param9", "param10"],
    "mast6": ["param7", "param8", "param9", "param10"],
    "mast7": ["param7", "param8", "param9", "param10"],
    "mast8": ["param7", "param8", "param9", "param10"],
    "mast9": ["param7", "param8", "param9", "param10"],
    "mast10": ["param7", "param8", "param9", "param10"],
    "mast11": ["param7", "param8", "param9", "param10"],
    "mast12": ["param7", "param8", "param9", "param10"],
}

LOCATIONS: Dict[str, Dict[str, Any]] = {
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
            {"coords": ["x", "y"], "system_type": "GeographicCRS",
             "system_id": "http://www.example.com/define/crs/geog_crs"},
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
            {"coords": ["x", "y"], "system_type": "GeographicCRS",
             "system_id": "http://www.example.com/define/crs/geog_crs"},
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
            {"coords": ["x", "y"], "system_type": "GeographicCRS",
             "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "gregorian"},
            {"coords": ["z"], "system_type": "VerticalRS", "system_id": "http://www.example.com/define/crs/vert_rs"},
        ],
    },
    "25364": {
        "geometry": Point(-3.0, 55.5),
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
            {"coords": ["x", "y"], "system_type": "GeographicCRS",
             "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "standard"},
        ],
    },
    "mast1": {
        "geometry": Point(-3.0, 55.5),
        "axes": ["x", "y", "t", "z"],
        "axis_x_values": {"values": [-3.0]},
        "axis_y_values": {"values": [55.5]},
        "axis_t_values": {"values": TEMPORAL_EXTENTS["00004"]["temporal_values"]},
        "axis_z_values": {"values": VERTICAL_EXTENTS["00004"]["vertical_values"]},
        "temporal_interval": TEMPORAL_EXTENTS["00004"]["temporal_interval"],
        "properties": {
            "name": "Observing mast site 1",
            "datetime": TEMPORAL_EXTENTS["00004"]["temporal_interval"][0],
            "detail": "http://www.example.com/define/location/mast1",
            "description": "A point location over a timeseries",
        },
        "referencing": [
            {"coords": ["x", "y"], "system_type": "GeographicCRS",
             "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "standard"},
            {"coords": ["z"], "system_type": "VerticalRS", "system_id": "http://www.example.com/define/crs/vert_rs"},
        ],
    },
    "mast2": {
        "geometry": Point(-2.6, 54.7),
        "axes": ["x", "y", "t", "z"],
        "axis_x_values": {"values": [-2.6]},
        "axis_y_values": {"values": [54.7]},
        "axis_t_values": {"values": TEMPORAL_EXTENTS["00004"]["temporal_values"]},
        "axis_z_values": {"values": VERTICAL_EXTENTS["00004"]["vertical_values"]},
        "temporal_interval": TEMPORAL_EXTENTS["00004"]["temporal_interval"],
        "properties": {
            "name": "Observing mast site 2",
            "datetime": TEMPORAL_EXTENTS["00004"]["temporal_interval"][0],
            "detail": "http://www.example.com/define/location/mast2",
            "description": "A point location over a timeseries",
        },
        "referencing": [
            {"coords": ["x", "y"], "system_type": "GeographicCRS",
             "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "standard"},
            {"coords": ["z"], "system_type": "VerticalRS", "system_id": "http://www.example.com/define/crs/vert_rs"},
        ],
    },
    "mast3": {
        "geometry": Point(-1.7, 55.0),
        "axes": ["x", "y", "t", "z"],
        "axis_x_values": {"values": [-1.7]},
        "axis_y_values": {"values": [55.0]},
        "axis_t_values": {"values": TEMPORAL_EXTENTS["00004"]["temporal_values"]},
        "axis_z_values": {"values": VERTICAL_EXTENTS["00004"]["vertical_values"]},
        "temporal_interval": TEMPORAL_EXTENTS["00004"]["temporal_interval"],
        "properties": {
            "name": "Observing mast site 3",
            "datetime": TEMPORAL_EXTENTS["00004"]["temporal_interval"][0],
            "detail": "http://www.example.com/define/location/mast3",
            "description": "A point location over a timeseries",
        },
        "referencing": [
            {"coords": ["x", "y"], "system_type": "GeographicCRS",
             "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "standard"},
            {"coords": ["z"], "system_type": "VerticalRS", "system_id": "http://www.example.com/define/crs/vert_rs"},
        ],
    },
    "mast4": {
        "geometry": Point(-1.2, 53.9),
        "axes": ["x", "y", "t", "z"],
        "axis_x_values": {"values": [-1.2]},
        "axis_y_values": {"values": [53.9]},
        "axis_t_values": {"values": TEMPORAL_EXTENTS["00004"]["temporal_values"]},
        "axis_z_values": {"values": VERTICAL_EXTENTS["00004"]["vertical_values"]},
        "temporal_interval": TEMPORAL_EXTENTS["00004"]["temporal_interval"],
        "properties": {
            "name": "Observing mast site 4",
            "datetime": TEMPORAL_EXTENTS["00004"]["temporal_interval"][0],
            "detail": "http://www.example.com/define/location/mast4",
            "description": "A point location over a timeseries",
        },
        "referencing": [
            {"coords": ["x", "y"], "system_type": "GeographicCRS",
             "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "standard"},
            {"coords": ["z"], "system_type": "VerticalRS", "system_id": "http://www.example.com/define/crs/vert_rs"},
        ],
    },
    "mast5": {
        "geometry": Point(-0.2, 53.1),
        "axes": ["x", "y", "t", "z"],
        "axis_x_values": {"values": [-0.2]},
        "axis_y_values": {"values": [53.1]},
        "axis_t_values": {"values": TEMPORAL_EXTENTS["00004"]["temporal_values"]},
        "axis_z_values": {"values": VERTICAL_EXTENTS["00004"]["vertical_values"]},
        "temporal_interval": TEMPORAL_EXTENTS["00004"]["temporal_interval"],
        "properties": {
            "name": "Observing mast site 5",
            "datetime": TEMPORAL_EXTENTS["00004"]["temporal_interval"][0],
            "detail": "http://www.example.com/define/location/mast5",
            "description": "A point location over a timeseries",
        },
        "referencing": [
            {"coords": ["x", "y"], "system_type": "GeographicCRS",
             "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "standard"},
            {"coords": ["z"], "system_type": "VerticalRS", "system_id": "http://www.example.com/define/crs/vert_rs"},
        ],
    },
    "mast6": {
        "geometry": Point(-0.55, 53.3),
        "axes": ["x", "y", "t", "z"],
        "axis_x_values": {"values": [-0.55]},
        "axis_y_values": {"values": [53.3]},
        "axis_t_values": {"values": TEMPORAL_EXTENTS["00004"]["temporal_values"]},
        "axis_z_values": {"values": VERTICAL_EXTENTS["00004"]["vertical_values"]},
        "temporal_interval": TEMPORAL_EXTENTS["00004"]["temporal_interval"],
        "properties": {
            "name": "Observing mast site 6",
            "datetime": TEMPORAL_EXTENTS["00004"]["temporal_interval"][0],
            "detail": "http://www.example.com/define/location/mast6",
            "description": "A point location over a timeseries",
        },
        "referencing": [
            {"coords": ["x", "y"], "system_type": "GeographicCRS",
             "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "standard"},
            {"coords": ["z"], "system_type": "VerticalRS", "system_id": "http://www.example.com/define/crs/vert_rs"},
        ],
    },
    "mast7": {
        "geometry": Point(-3.4, 50.7),
        "axes": ["x", "y", "t", "z"],
        "axis_x_values": {"values": [-3.4]},
        "axis_y_values": {"values": [50.7]},
        "axis_t_values": {"values": TEMPORAL_EXTENTS["00004"]["temporal_values"]},
        "axis_z_values": {"values": VERTICAL_EXTENTS["00004"]["vertical_values"]},
        "temporal_interval": TEMPORAL_EXTENTS["00004"]["temporal_interval"],
        "properties": {
            "name": "Observing mast site 7",
            "datetime": TEMPORAL_EXTENTS["00004"]["temporal_interval"][0],
            "detail": "http://www.example.com/define/location/mast7",
            "description": "A point location over a timeseries",
        },
        "referencing": [
            {"coords": ["x", "y"], "system_type": "GeographicCRS",
             "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "standard"},
            {"coords": ["z"], "system_type": "VerticalRS", "system_id": "http://www.example.com/define/crs/vert_rs"},
        ],
    },
    "mast8": {
        "geometry": Point(-1.2, 51.2),
        "axes": ["x", "y", "t", "z"],
        "axis_x_values": {"values": [-1.2]},
        "axis_y_values": {"values": [51.2]},
        "axis_t_values": {"values": TEMPORAL_EXTENTS["00004"]["temporal_values"]},
        "axis_z_values": {"values": VERTICAL_EXTENTS["00004"]["vertical_values"]},
        "temporal_interval": TEMPORAL_EXTENTS["00004"]["temporal_interval"],
        "properties": {
            "name": "Observing mast site 1",
            "datetime": TEMPORAL_EXTENTS["00004"]["temporal_interval"][0],
            "detail": "http://www.example.com/define/location/mast1",
            "description": "A point location over a timeseries",
        },
        "referencing": [
            {"coords": ["x", "y"], "system_type": "GeographicCRS",
             "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "standard"},
            {"coords": ["z"], "system_type": "VerticalRS", "system_id": "http://www.example.com/define/crs/vert_rs"},
        ],
    },
    "mast9": {
        "geometry": Point(-0.8, 51.3),
        "axes": ["x", "y", "t", "z"],
        "axis_x_values": {"values": [-0.8]},
        "axis_y_values": {"values": [51.3]},
        "axis_t_values": {"values": TEMPORAL_EXTENTS["00004"]["temporal_values"]},
        "axis_z_values": {"values": VERTICAL_EXTENTS["00004"]["vertical_values"]},
        "temporal_interval": TEMPORAL_EXTENTS["00004"]["temporal_interval"],
        "properties": {
            "name": "Observing mast site 9",
            "datetime": TEMPORAL_EXTENTS["00004"]["temporal_interval"][0],
            "detail": "http://www.example.com/define/location/mast9",
            "description": "A point location over a timeseries",
        },
        "referencing": [
            {"coords": ["x", "y"], "system_type": "GeographicCRS",
             "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "standard"},
            {"coords": ["z"], "system_type": "VerticalRS", "system_id": "http://www.example.com/define/crs/vert_rs"},
        ],
    },
    "mast10": {
        "geometry": Point(-0.4, 51.5),
        "axes": ["x", "y", "t", "z"],
        "axis_x_values": {"values": [-0.4]},
        "axis_y_values": {"values": [51.5]},
        "axis_t_values": {"values": TEMPORAL_EXTENTS["00004"]["temporal_values"]},
        "axis_z_values": {"values": VERTICAL_EXTENTS["00004"]["vertical_values"]},
        "temporal_interval": TEMPORAL_EXTENTS["00004"]["temporal_interval"],
        "properties": {
            "name": "Observing mast site 10",
            "datetime": TEMPORAL_EXTENTS["00004"]["temporal_interval"][0],
            "detail": "http://www.example.com/define/location/mast10",
            "description": "A point location over a timeseries",
        },
        "referencing": [
            {"coords": ["x", "y"], "system_type": "GeographicCRS",
             "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "standard"},
            {"coords": ["z"], "system_type": "VerticalRS", "system_id": "http://www.example.com/define/crs/vert_rs"},
        ],
    },
    "mast11": {
        "geometry": Point(0.1, 51.5),
        "axes": ["x", "y", "t", "z"],
        "axis_x_values": {"values": [0.1]},
        "axis_y_values": {"values": [51.5]},
        "axis_t_values": {"values": TEMPORAL_EXTENTS["00004"]["temporal_values"]},
        "axis_z_values": {"values": VERTICAL_EXTENTS["00004"]["vertical_values"]},
        "temporal_interval": TEMPORAL_EXTENTS["00004"]["temporal_interval"],
        "properties": {
            "name": "Observing mast site 11",
            "datetime": TEMPORAL_EXTENTS["00004"]["temporal_interval"][0],
            "detail": "http://www.example.com/define/location/mast10",
            "description": "A point location over a timeseries",
        },
        "referencing": [
            {"coords": ["x", "y"], "system_type": "GeographicCRS",
             "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "standard"},
            {"coords": ["z"], "system_type": "VerticalRS", "system_id": "http://www.example.com/define/crs/vert_rs"},
        ],
    },
    "mast12": {
        "geometry": Point(0.1, 52.1),
        "axes": ["x", "y", "t", "z"],
        "axis_x_values": {"values": [0.1]},
        "axis_y_values": {"values": [52.1]},
        "axis_t_values": {"values": TEMPORAL_EXTENTS["00004"]["temporal_values"]},
        "axis_z_values": {"values": VERTICAL_EXTENTS["00004"]["vertical_values"]},
        "temporal_interval": TEMPORAL_EXTENTS["00004"]["temporal_interval"],
        "properties": {
            "name": "Observing mast site 12",
            "datetime": TEMPORAL_EXTENTS["00004"]["temporal_interval"][0],
            "detail": "http://www.example.com/define/location/mast12",
            "description": "A point location over a timeseries",
        },
        "referencing": [
            {"coords": ["x", "y"], "system_type": "GeographicCRS",
             "system_id": "http://www.example.com/define/crs/geog_crs"},
            {"coords": ["t"], "system_type": "TemporalRS", "system_calendar": "standard"},
            {"coords": ["z"], "system_type": "VerticalRS", "system_id": "http://www.example.com/define/crs/vert_rs"},
        ],
    },
}
