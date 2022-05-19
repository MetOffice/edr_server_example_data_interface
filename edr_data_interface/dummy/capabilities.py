from typing import List

from edr_server.abstract_data_interface.capabilities import API, APIData, Capabilities, CapabilitiesData, Conformance


class API(API):
    def data(self) -> APIData:
        return APIData


class Capabilities(Capabilities):
    def data(self) -> CapabilitiesData:
        data = {
            "title": "A dummy example",
            "description": "This is a dummy example of templating a capabilities request.",
            "keywords": ["Example", "Dummy"],
            "provider_name": "Galadriel",
            "provider_url": "",
            "contact_email": "dummy@example.com",
            "contact_phone": "07987 654321",
            "contact_fax": "",
            "contact_hours": "9 til 5",
            "contact_instructions": "Don't",
            "contact_address": "Over there",
            "contact_postcode": "ZZ99 9ZZ",
            "contact_city": "Neverland",
            "contact_state": "",
            "contact_country": "Wakanda",
        }
        return CapabilitiesData(**data)


class Conformance(Conformance):
    def data(self) -> List:
        return ["example", "dummy"]
