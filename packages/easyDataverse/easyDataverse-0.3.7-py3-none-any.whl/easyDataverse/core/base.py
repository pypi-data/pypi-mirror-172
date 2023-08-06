import json
import yaml
import xmltodict

from enum import Enum
from pydantic import BaseModel
from typing import Dict


class DataverseBase(BaseModel):
    class Config:
        validate_all = True
        validate_assignment = True
        use_enum_values = True

    @classmethod
    def from_json_string(cls, json_string: str):
        """Initializes an object from a JSON file"""

        return cls.parse_obj(json.loads(json_string))

    @classmethod
    def from_json_file(cls, file_path: str):
        """Initializes an object from a JSON file"""

        with open(file_path, "r") as f:
            return cls.parse_obj(json.load(f))

    @classmethod
    def from_yaml_string(cls, yaml_string: str):
        """Initializes an object from a YAML string"""

        return cls.parse_obj(yaml.safe_load(yaml_string))

    @classmethod
    def from_yaml_file(cls, file_path: str):
        """Initializes an object from a YAML string"""

        with open(file_path, "r") as f:
            return cls.parse_obj(yaml.safe_load(f))

    def json(self, indent: int = 2, **kwargs) -> str:
        """Returns a JSON representation of the dataverse object."""

        # Read the JSON to filter empty compounds
        json_obj = json.loads(super().json(exclude_none=True, indent=indent, **kwargs))

        return json.dumps(
            {key: value for key, value in json_obj.items() if value != []},
            indent=indent,
        )

    def yaml(self):
        """Returns a YAML representation of the dataverse object"""

        yaml_obj = self.dict(exclude_none=True)

        return yaml.safe_dump(
            yaml_obj,
        )

    def dict(self, **dictkwargs) -> Dict:
        """Returns a dictionary representation of the dataverse object."""

        # Get the dictionary function from pyDantic
        fields = super().dict(**dictkwargs)

        return {key: value for key, value in fields.items() if value != []}

    def xml(self, **dictkwargs) -> str:
        """Returns an XML representation of the dataverse object."""

        # Turn all fields to camel case
        fields = self._keys_to_camel({self.__class__.__name__: self.dict(**dictkwargs)})

        return xmltodict.unparse(fields, pretty=True, indent="    ")

    def _keys_to_camel(self, dictionary: Dict):
        nu_dict = {}
        for key in dictionary.keys():
            if isinstance(dictionary[key], dict):
                nu_dict[self._snake_to_camel(key)] = self._keys_to_camel(
                    dictionary[key]
                )
            else:
                nu_dict[self._snake_to_camel(key)] = dictionary[key]
        return nu_dict

    @staticmethod
    def _snake_to_camel(word: str) -> str:
        return "".join(x.capitalize() or "_" for x in word.split("_"))

    def dataverse_dict(self) -> Dict:
        """Converts a metadatablock object model to the appropriate dataverse JSON format"""

        # Get properties and init json_obj
        json_obj = {}

        for attr, field in self.__fields__.items():

            if any(name in attr for name in ["add_", "_metadatablock_name"]):
                # Only necessary for blind fetch
                continue

            # Fetch the value of the attribute
            properties = field.field_info.extra
            value = getattr(self, attr)

            if value == [] or value is None:
                # Guard clause to catch empty compounds
                continue

            # Process compounds
            if properties["typeClass"] == "compound":
                value = [field.dataverse_dict() for field in value]

            # Assign everything
            if isinstance(value, list):
                # TODO Refactor to separate check
                if all(isinstance(val, Enum) for val in value):
                    value = [val.value for val in value]

            json_obj.update(
                {
                    properties["typeName"]: {
                        "multiple": properties["multiple"],
                        "typeClass": properties["typeClass"],
                        "typeName": properties["typeName"],
                        "value": value if isinstance(value, list) else str(value),
                    }
                }
            )

        if hasattr(self, "_metadatablock_name"):
            return {
                getattr(self, "_metadatablock_name"): {
                    "fields": list(json_obj.values())
                }
            }
        else:
            return json_obj

    def to_dataverse_json(self, indent: int = 2) -> str:
        """Returns a JSON formatted representation of the dataverse object."""
        return json.dumps(self.dataverse_dict(), indent=indent)
