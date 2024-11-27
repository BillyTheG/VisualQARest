from pathlib import Path
from configparser import ConfigParser

from pydantic.v1 import BaseSettings, BaseModel


class ConfigParserSource:
    def __init__(self, config_file: str):
        self.config_file = config_file

    def __call__(self, *args, **kwargs):
        path = Path(self.config_file).expanduser()
        if not path.exists():
            return {}
        if not path.is_file():
            raise Exception(f"{path.absolute()} is not a file")

        config_parser = ConfigParser()
        config_parser.read(self.config_file)
        config_dict = {s.lower(): dict(config_parser.items(s)) for s in config_parser.sections()}
        return config_dict


class LoggerConfig(BaseModel):
    logfile: str


class DataBaseConfig(LoggerConfig):
    driver: str = "mariadb"
    host: str
    database: str
    user: str
    password: str
    port: int


class SpacyConfig(BaseModel):
    path: str


class ModelConfig(BaseModel):
    path: str
    binary: bool


class ServiceConfig(BaseSettings):
    database: DataBaseConfig
    spacy: SpacyConfig
    model: ModelConfig

    class Config:
        env_nested_delimiter = "__"
        config_file = "../Resources/geo_reference.ini"

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return init_settings, env_settings, ConfigParserSource(config_file=cls.config_file), file_secret_settings
