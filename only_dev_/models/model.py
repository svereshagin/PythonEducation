import pathlib

from pydantic import BaseModel, Field
from typing import Dict, Any
import math
import json
import hashlib
import sqlite3
from constant_file_roots import *

first_key_path = Path(__file__).parent.parent.parent.joinpath(
    "src/First_level/first_key.md"
)
second_key_path = Path(__file__).parent.parent.parent.joinpath(
    "src/Second_level/second_key.md"
)
third_key_path = Path(__file__).parent.parent.parent.joinpath(
    "src/Third_level/third_key.md"
)
fourth_key_path = Path(__file__).parent.parent.parent.joinpath(
    "src/Fourth_level/fourth_key"
)


class TestFileCreateModel(BaseModel):
    hash_id_1: Dict[str, Any] = Field(default_factory=lambda: {"hex": math.nan})
    path: Path = Field(
        default=Path(__file__).parent.parent.parent.joinpath(
            "secrets/secret/very_secret"
        )
    )
    First_level: Dict[str, Any] = Field(
        default_factory=lambda: {
            "test1": math.nan,
            "test2": math.nan,
            "test3": math.nan,
            "test4": math.nan,
        }
    )
    Second_level: Dict[str, Any] = Field(
        default_factory=lambda: {
            "test6": math.nan,
            "test7": math.nan,
            "test8": math.nan,
            "test9": math.nan,
        }
    )
    Third_level: Dict[str, Any] = Field(
        default_factory=lambda: {
            "test11": math.nan,
            "test12": math.nan,
            "test13": math.nan,
            "test14": math.nan,
        }
    )
    Fourth_level: Dict[str, Any] = Field(
        default_factory=lambda: {
            "test16": math.nan,
            "test17": math.nan,
            "test18": math.nan,
            "test19": math.nan,
        }
    )
    #прописать функцию проверки конкретного теста из выборки
    def change_test_result(self, module: str, test_n: str):
        with open(self.path.joinpath("secret_key.json"), "r") as file:
            data = json.load(file)
        data[module][test_n] = "OK"
        with open(self.path.joinpath("secret_key.json"), "w") as file:
            json.dump(data, fp=file, indent=4)

    def generate_hash_value(self, module: str, exp = 10):
        if self.check_all_module_tests(module):
            hash_object = hashlib.sha256((module + str(exp)).encode("utf-8"))
            # Преобразуем хеш в строку
            unique_hash = hash_object.hexdigest()


    def check_all_module_tests(self, module: str):
        """Если все тесты проходят, возвращаем модуль, иначе возвращаем None"""
        with open(self.path.joinpath("secret_key.json"), "r") as f:
            data = json.load(f)
        if module in data and isinstance(data[module], dict):
            tests = data[module]
            # Проверяем, что все значения в тестах равны "OK"
            if all(value == "OK" for value in tests.values()):
                return module
            else:
                print(f"Некоторые тесты модуля '{module}' не пройдены.")
        else:
            print(
                f"Ошибка: модуль '{module}' не найден или данные не являются словарем."
            )
        return None

    def init_json(self):
        def convert_nan_to_none(value):
            if isinstance(value, dict):
                return {k: convert_nan_to_none(v) for k, v in value.items()}
            elif isinstance(value, float) and math.isnan(value):
                return None
            return value

        self.path.mkdir(parents=True, exist_ok=True)
        self.path.joinpath("secret_key.json").touch(exist_ok=True, mode=0o755)
        model_dict = self.model_dump(exclude={"path"})
        model_dict = {k: convert_nan_to_none(v) for k, v in model_dict.items()}

        with open(self.path.joinpath("secret_key.json"), "w") as file:
            json.dump(model_dict, file, indent=4)


class SQL_LOGGER_shema:
    def __init__(self, ) -> None:
        PreCreatingProjectFiles()
        self.create_main_table()

    def create_main_table(self):
        query = ("""CREATE TABLE IF NOT EXISTS users (
                attempt INTEGER PRIMARY KEY,
                quest_num INTEGER,
                quest_result BOOL,
                file_text VARCHAR
        ) """)
        with sqlite3.connect(sql_database_file) as conn:
            c = conn.cursor()
            c.execute(query)
            conn.commit()

    def insert_data(self, quest_num: int, quest_result: int, file_text: str) -> None:
        query = """INSERT INTO users (quest_num, quest_result, file_text) VALUES (?, ?, ?)"""
        with sqlite3.connect(sql_database_file) as conn:
            c = conn.cursor()
            c.execute(query, (quest_num, quest_result, file_text))
            conn.commit()


class PreCreatingProjectFiles:
    sql_database_path.mkdir(parents=True, exist_ok=True, mode=0o755)
    sql_database_file.touch(mode=0o755, exist_ok=True)

    @staticmethod
    def _make_key(module_num: int):
        file = 'main_' + str(module_num)
        file_with_key = {
            1: ['first_key', 'First_level'],
            2: ['second_key', 'Second_level'],
            3: ['third_key', 'Third_level'],
            4: ['fourth_key', 'Fourth_key']
        }
        file = project_files_for_test[file].parent.joinpath(f"{file_with_key[module_num[0]]}_key.md")
        with open(file, 'w') as f:
            hash = TestFileCreateModel().generate_hash_value(file_with_key[module_num][1])
            f.write(str(hash))


pathlib.Path(__file__).joinpath().mkdir()

