from ...abstract.capabilities import API, Capabilities, Conformance


class API(API):
    def data(self):
        return None


class Capabilities(Capabilities):
    def data(self):
        return {
            "title": "A dummy example",
            "description": "This is a dummy example of templating a capabilities request.",
            "links_api_href": self.api_link_href,
            "links_conformance_href": self.conformance_link_href,
            "links_collections_href": self.collections_link_href,
            "keywords": ["Example", "Dummy"],
            "provider_name": "Galadriel",
            "provider_url": None,
            "contact_email": "dummy@example.com",
            "contact_phone": "07987 654321",
            "contact_fax": None,
            "contact_hours": "9 til 5",
            "contact_instructions": "Don't",
            "contact_address": "Over there",
            "contact_postcode": "ZZ99 9ZZ",
            "contact_city": "Neverland",
            "contact_state": "",
            "contact_country": "Wakanda",
        }


class Conformance(Conformance):
    def data(self):
        return ["example", "dummy"]
