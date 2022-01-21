from .core import Interface


class API(Interface):
    pass


class Capabilities(Interface):
    def __init__(
        self,
        api_link_href: str,
        collections_link_href: str,
        conformance_link_href: str,
    ) -> None:
        self.api_link_href = api_link_href
        self.collections_link_href = collections_link_href
        self.conformance_link_href = conformance_link_href


class Conformance(Interface):
    pass