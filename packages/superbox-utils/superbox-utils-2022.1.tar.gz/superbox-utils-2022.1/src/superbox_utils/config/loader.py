import dataclasses
from dataclasses import dataclass
from dataclasses import is_dataclass
from pathlib import Path
from typing import Any
from typing import NamedTuple
from typing import Union

from superbox_utils.config.exception import ConfigException
from superbox_utils.yaml.loader import yaml_loader_safe


class RegexValidation(NamedTuple):
    regex: str
    error: str


class Validation:
    ALLOWED_CHARACTERS: RegexValidation = RegexValidation(
        regex=r"^[A-Za-z\d_-]*$", error="The following characters are prohibited: a-z 0-9 -_"
    )


@dataclass
class ConfigLoaderMixin:
    def update(self, new):
        for key, value in new.items():
            if hasattr(self, key):
                item = getattr(self, key)

                if is_dataclass(item):
                    item.update(value)
                else:
                    setattr(self, key, value)

        self.validate()

    def update_from_yaml_file(self, config_path: Path):
        if config_path.exists():
            yaml_data: Union[dict, list] = yaml_loader_safe(config_path)

            if isinstance(yaml_data, dict):
                self.update(yaml_data)

    def validate(self):
        for _field in dataclasses.fields(self):
            value: Any = getattr(self, _field.name)

            if is_dataclass(value):
                value.validate()
            else:
                if method := getattr(self, f"_validate_{_field.name}", None):
                    setattr(self, _field.name, method(getattr(self, _field.name), _field=_field))

                if not isinstance(value, _field.type) and not is_dataclass(value):
                    raise ConfigException(f"Expected {_field.name} to be {_field.type}, got {repr(value)}")
