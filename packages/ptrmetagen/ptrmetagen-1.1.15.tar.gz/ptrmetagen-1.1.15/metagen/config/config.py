from pydantic import BaseModel, Field, AnyUrl
import yaml
from typing import Literal, Optional
from pathlib import Path

BASE_CONFIG_FILE = Path(__file__).parent / 'config.yaml'


class RegisterConfig(BaseModel):
    registerName: Literal['pandas', 'dict']

    def __str__(self):
        return '\n'.join([f"- {k} : {v}" for k, v in self.__dict__.items()])


class ImporterConfig(BaseModel):
    path: Optional[str]
    instance_url: Optional[str]
    host: Optional[str]

    def __str__(self):
        return '\n'.join([f"- {k} : {v}" for k, v in self.__dict__.items()])


class Config(BaseModel):
    register_setting: RegisterConfig = Field(default_factory=RegisterConfig)
    importer_setting: ImporterConfig = Field(default_factory=ImporterConfig)

    @classmethod
    def load(cls):
        data = load_yaml('config.yaml')
        return cls(**data)

    def save(self):
        dump_yaml(Path('config.yaml'), self.dict())

    def __str__(self):
        return '\n'.join([f"- {k} : \n \t {str(v)}" for k, v in self.__dict__.items()])


def load_yaml(path: str) -> dict:
    with open(path, 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def dump_yaml(path: Path, data: dict) -> None:
    with open(path, 'w') as file:
        file.write(yaml.dump(data, Dumper=yaml.Dumper))


if __name__ == '__main__':
    config = Config.load()
    config.importer_setting.host = 'http://localhost:8000/metadata'
    config.save()



