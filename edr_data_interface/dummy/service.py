from edr_server.abstract_data_interface.service import Service, ServiceData

URLS = {
    "description_url": "https://www.example.org/service/description.html",
    "license_url": "https://www.example.org/service/licence.html",
    "terms_url": "https://www.example.org/service/terms-and-conditions.html",
}


class Service(Service):
    def data(self) -> ServiceData:
        return ServiceData(**URLS)
