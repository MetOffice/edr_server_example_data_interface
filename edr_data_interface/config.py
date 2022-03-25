from pathlib import Path
import yaml
from yaml.loader import SafeLoader


class Config(object):
    def __init__(self):
        self.yaml_path = self._yaml_path()
        self._yaml = None

    @property
    def yaml(self):
        if self._yaml is None:
            self.load_yaml()
        return self._yaml

    @yaml.setter
    def yaml(self, value):
        self._yaml = value

    def _yaml_path(self):
        relative_path = "etc/data_config.yml"
        app_root = Path(__file__).parents[1]
        return (app_root / Path(relative_path)).absolute()

    def load_yaml(self):
        """Load the config YAML file for parsing."""
        with open(self.yaml_path, "r") as oyfh:
            self.yaml = yaml.load(oyfh, Loader=SafeLoader)

    def data_source(self):
        return self.yaml["data"]["source"]

    def cloud_data_provider(self):
        provider = self.yaml["cloud"]["provider"]
        object_store = self.yaml["cloud"]["object_store_name"]
        path = self.yaml["cloud"]["object_store_path"]
        file_pattern = self.yaml["cloud"]["file_pattern"]
        return provider, object_store, path, file_pattern

    def local_data_provider(self):
        path = self.yaml["local"]["path"]
        file_pattern = self.yaml["local"]["file_pattern"]
        return path, file_pattern

    def cloud_protocol(self, provider=None):
        if provider is None:
            provider, _ = self.cloud_data_provider()
        if self.data_source() == "cloud":
            protocol = "s3" if provider.lower() in ["s3", "aws"] else "https"
        else:
            protocol = None
        return protocol

    def data_path(self):
        source = self.data_source()
        if source == "cloud":
            provider, object_store, path, file_pattern = self.cloud_data_provider()
            protocol = self.cloud_protocol(provider)
            data_path = f"{protocol}://{object_store}/{path}/{file_pattern}"
        elif source == "local":
            path, file_pattern = self.local_data_provider()
            data_path = Path(path) / Path(file_pattern)
        else:
            raise ValueError("Unsupported data source.")
        return data_path


config = Config()