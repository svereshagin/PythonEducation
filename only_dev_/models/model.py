from pydantic import BaseModel, Field
from typing import Dict, Any
import math
import json
from pathlib import Path
import hashlib

first_key_path = Path(__file__).parent.parent.parent.joinpath("src/First_level/first_key.md")
second_key_path = Path(__file__).parent.parent.joinpath("src/Second_level/second_key.md")
third_key_path = Path(__file__).parent.parent.joinpath("src/Third_level/third_key.md")
fourth_key_path = Path(__file__).parent.parent.joinpath("src/Fourth_level/fourth_key")

class TestFileCreateModel(BaseModel):
    hash_id_1: Dict[str, Any] = Field(default_factory=lambda: {'hex': math.nan})
    path: Path = Field(default=Path(__file__).parent.parent.parent.joinpath("secrets/secret/very_secret"))
    first_key: Dict[str, Any] = Field(
        default_factory=lambda: {
            "test1": math.nan,
            "test2": math.nan,
            "test3": math.nan,
            "test4": math.nan,
            "test5": math.nan,
        }
    )
    second_key: Dict[str, Any] = Field(
        default_factory=lambda: {
            "test6": math.nan,
            "test7": math.nan,
            "test8": math.nan,
            "test9": math.nan,
            "test10": math.nan,
        }
    )
    third_key: Dict[str, Any] = Field(
        default_factory=lambda: {
            "test11": math.nan,
            "test12": math.nan,
            "test13": math.nan,
            "test14": math.nan,
            "test15": math.nan,
        }
    )
    fourth_key: Dict[str, Any] = Field(
        default_factory=lambda: {
            "test16": math.nan,
            "test17": math.nan,
            "test18": math.nan,
            "test19": math.nan,
            "test20": math.nan,
        }
    )
    def change_test_result(self, module: str, test_n: str):
        with open(self.path.joinpath('secret_key.json'), "r") as file:
            data = json.load(file)
        data[module][test_n] = 'OK'
        with open(self.path.joinpath('secret_key.json'), "w") as file:
            json.dump(data, fp=file, indent=4)

    def generate_hash_value(self, module: str, exp: int = 10):
        if self.check_all_module_tests(module):
            hash_object = hashlib.sha256((module+str(exp)).encode('utf-8'))
            # Преобразуем хеш в строку
            unique_hash = hash_object.hexdigest()
            print(f"Generated hash: {unique_hash}") #добавить игровой формат
            with open(first_key_path, mode='w') as f:
                f.write(unique_hash)

    def check_all_module_tests(self, module: str):
        """Если все тесты проходят, возвращаем модуль, иначе возвращаем None"""
        with open(self.path.joinpath('secret_key.json'), "r") as f:
            data = json.load(f)
        if module in data and isinstance(data[module], dict):
            tests = data[module]
            # Проверяем, что все значения в тестах равны "OK"
            if all(value == "OK" for value in tests.values()):
                return module
            else:
                print(f"Некоторые тесты модуля '{module}' не пройдены.")
        else:
            print(f"Ошибка: модуль '{module}' не найден или данные не являются словарем.")
        return None

    def init_json(self):
        def convert_nan_to_none(value):
            if isinstance(value, dict):
                return {k: convert_nan_to_none(v) for k, v in value.items()}
            elif isinstance(value, float) and math.isnan(value):
                return None
            return value
        self.path.mkdir(parents=True, exist_ok=True)
        self.path.joinpath('secret_key.json').touch(exist_ok=True, mode=0o755)
        model_dict = self.model_dump(exclude={"path"})
        model_dict = {k: convert_nan_to_none(v) for k, v in model_dict.items()}

        with open(self.path.joinpath('secret_key.json'), "w") as file:
            json.dump(model_dict, file, indent=4)














# class TestFileCreateUpdater(TestFileCreateModel):
#     def check_hash(self, module: str) -> bool:
#         """Проверяет наличие значения 'hash' для модуля."""
#         with open(secret_file, mode="r") as f:
#             data = json.load(f)
#         return data[module].get('hash') is not None  # Проверяем, что 'hash' не None
#
#     def check_keys(self, module: str) -> bool:
#         """Проверяет, что все ключи внутри модуля не равны None."""
#         with open(secret_file, mode="r") as f:
#             data = json.load(f)
#
#         # Получаем ключи модуля и проверяем их значения
#         keys_values = data.get(module, {})
#         return all(value is not None for value in keys_values.values())
#
#     def create_hash_from_values(self, module: str) -> None:
#         """Создаёт хэш из всех значений ключей внутри модуля."""
#         with open(secret_file, mode="r") as f:
#             data = json.load(f)
#
#         # Получаем значения всех ключей
#         keys_values = data.get(module, {})
#
#         # Конкатенируем все значения ключей
#         concatenated_values = ''.join(str(value) for value in keys_values.values())
#
#         # Создаём хэш
#         hash_value = hashlib.sha256(concatenated_values.encode()).hexdigest()
#
#         # Обновляем хэш в JSON-файле
#         data[module]['hash'] = hash_value
#
#         with open(secret_file, mode="w") as f:
#             json.dump(data, f, indent=4)
#
#     def update_and_create_hash(self, module: str) -> None:
#         """Записывает значение и создаёт хэш, если все ключи не равны None."""
#         self.change_key_value(module, "update_value", 1)  # Записываем значение (например, 1)
#         if self.check_keys(module):
#             self.create_hash_from_values(module)  # Создаём хэш, если все ключи не равны None



