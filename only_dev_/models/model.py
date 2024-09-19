from pydantic import BaseModel, Field
from typing import Dict, Any
import math
import json
from constants import secret_file
from pathlib import Path


class KeyModel(BaseModel):
    first_key: Dict[str, Any] = Field(
        default_factory=lambda: {
            "key1": math.nan,
            "key2": math.nan,
            "key3": math.nan,
            "key4": math.nan,
        }
    )
    second_key: Dict[str, Any] = Field(
        default_factory=lambda: {
            "key1": math.nan,
            "key2": math.nan,
            "key3": math.nan,
            "key4": math.nan,
        }
    )
    third_key: Dict[str, Any] = Field(
        default_factory=lambda: {
            "key1": math.nan,
            "key2": math.nan,
            "key3": math.nan,
            "key4": math.nan,
        }
    )
    fourth_key: Dict[str, Any] = Field(
        default_factory=lambda: {
            "key1": math.nan,
            "key2": math.nan,
            "key3": math.nan,
            "key4": math.nan,
        }
    )

    def set_key_to_true(self, key_name: str):
        if key_name not in self.__annotations__:
            raise ValueError(f"Key {key_name} does not exist in the model.")

        current_value = getattr(self, key_name)
        if not isinstance(current_value, dict):
            raise ValueError(f"The value of {key_name} is not a dictionary.")

        updated_key = {subkey: True for subkey in current_value}
        setattr(self, key_name, updated_key)

    def init_json(self, path):
        def convert_nan_to_none(value):
            if isinstance(value, dict):
                return {k: convert_nan_to_none(v) for k, v in value.items()}
            elif isinstance(value, float) and math.isnan(value):
                return None
            return value

        model_dict = self.dict()
        model_dict = {k: convert_nan_to_none(v) for k, v in model_dict.items()}

        with open(path, "w") as file:
            json.dump(model_dict, file, indent=4)


class KeyUpdater(KeyModel):
    @staticmethod
    def change_key_value(module: str, key: str, update: Any) -> None:
        with open(file=secret_file, mode="r") as f:
            data = json.load(f)

        with open(file=secret_file, mode="w") as f:
            data[module][key] = update  # Тут нужно записать значение обновления
            json.dump(data, f, indent=4)


class MakePath(Path):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def create_path_if_not_exists(self, path: Path):
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True, mode=0o755)
            secret_file = path.joinpath("secret_key.json")
            secret_file.touch(exist_ok=True, mode=0o755)
            res = "path was created"
        else:
            res = "path already exists"
        return res
