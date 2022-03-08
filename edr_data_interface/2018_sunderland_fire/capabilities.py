from typing import List

from edr_server.abstract_data_interface.capabilities import (
    API, Capabilities, Conformance,
    APIData, CapabilitiesData)


class API(API):
    def data(self) -> APIData:
        return APIData


class Capabilities(Capabilities):
    def data(self) -> CapabilitiesData:
        data = {
            "title": "EDR Demonstrator - Sunderland Fire",
            "description": "Example of serving data using EDR (not for operational use).",
            "keywords": [
                "position",
                "location",
                "item",
                "namis",
                "data",
                "api",
            ],
            "provider_name": "Met Office",
            "provider_url": "https://www.metoffice.gov.uk",
            "contact_email": "dummy@example.com",
            "contact_phone": "",
            "contact_fax": "",
            "contact_hours": "",
            "contact_instructions": "Not at weekends",
            "contact_address": "The Met Office",
            "contact_postcode": "ZZ99 9ZZ",
            "contact_city": "Exeter",
            "contact_state": "",
            "contact_country": "UK",
        }
        return CapabilitiesData(**data)


class Conformance(Conformance):
    def data(self) -> List:
        return [
            "http://www.opengis.net/spec/ogcapi-common-1/1.0/conf/core",
            "http://www.opengis.net/spec/ogcapi-common-2/1.0/conf/collections",
            "http://www.opengis.net/spec/ogcapi-edr-1/1.0/conf/core",
            "http://www.opengis.net/spec/ogcapi-edr-1/1.0/conf/oas30",
            "http://www.opengis.net/spec/ogcapi-edr-1/1.0/conf/html",
            "http://www.opengis.net/spec/ogcapi-edr-1/1.0/conf/geojson",
            "http://www.opengis.net/spec/ogcapi-edr-1/1.0/conf/coveragejson",
            "http://www.opengis.net/spec/ogcapi-edr-1/1.0/conf/wkt"
        ]
