from .core import Interface


class RefreshCollections(Interface):
    def collection(self, name):
        raise NotImplemented

    def collections(self):
        raise NotImplemented

    def data(self):
        return self.collections()