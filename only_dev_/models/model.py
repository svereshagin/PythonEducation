import datetime
from pydantic import BaseModel, Field
from typing import Dict, Any, ClassVar
import math
import json
from pathlib import Path
import hashlib
import logging
from logging import FileHandler
import sqlite3


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
    first_key: Dict[str, Any] = Field(
        default_factory=lambda: {
            "test1": math.nan,
            "test2": math.nan,
            "test3": math.nan,
            "test4": math.nan,
        }
    )
    second_key: Dict[str, Any] = Field(
        default_factory=lambda: {
            "test6": math.nan,
            "test7": math.nan,
            "test8": math.nan,
            "test9": math.nan,
        }
    )
    third_key: Dict[str, Any] = Field(
        default_factory=lambda: {
            "test11": math.nan,
            "test12": math.nan,
            "test13": math.nan,
            "test14": math.nan,
        }
    )
    fourth_key: Dict[str, Any] = Field(
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

    def generate_hash_value(self, module: str, exp: int = 10):
        if self.check_all_module_tests(module):
            hash_object = hashlib.sha256((module + str(exp)).encode("utf-8"))
            # Преобразуем хеш в строку
            unique_hash = hash_object.hexdigest()
            print(f"Generated hash: {unique_hash}")  # добавить игровой формат
            with open(first_key_path, mode="w") as f:
                f.write(unique_hash)

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
        self.db_path = Path(__file__).parent.parent.parent.joinpath(
    "Info_Students/stats.sql"
)
        self._create_table()

    def _create_table(self):
        """Создание таблицы, если её ещё нет."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()

            # Создание таблиц для квестов
            for quest in ['quest1', 'quest2', 'quest3', 'quest4']:
                query = f"""
                    CREATE TABLE IF NOT EXISTS {quest} (
                        attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_quest_start_time TIMESTAMP,
                        first_quest_final_time TIMESTAMP,
                        result REAL,
                        description VARCHAR
                    )
                    """
                c.execute(query)
            query = """ CREATE TABLE IF NOT EXISTS users (name VARCHAR(255) UNIQUE) """
            # Таблица пользователей
            c.execute(query)

            # Добавляем пользователя из файла
            name = self.get_name_out_of_file()
            if name:
                self.add_user(name)

            conn.commit()

    def add_user(self, name: str) -> int:
        try:
            query = "SELECT name FROM users WHERE name = ?"
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute(query, (name,))

                # Проверяем, если пользователь существует
                user = c.fetchone()
                if user is None:
                    # Если пользователь не найден, добавляем его
                    c.execute("INSERT INTO users (name) VALUES (?)", (name,))
                    conn.commit()
                    return c.lastrowid  # Возвращаем id нового пользователя
                else:
                    print(f"Пользователь с именем '{name}' уже существует.")
                    return -1  # Возвращаем -1, если пользователь существует
        except sqlite3.Error as e:
            print(f"Ошибка: {e}")
            return -1

    def get_name_out_of_file(self):
        with open(Path(__file__).parent.parent.parent.joinpath("Name"), mode="r", encoding="utf-8") as file:
            for line in file:
                name = line.strip()
                if name:  # Условие проверяет, что строка не пустая
                    return name
            return None  # Если не найдено подходящего имени

    def insert_quest_data(self, quest: str, filename: Path, result: float, time_mod=None, time: datetime = None):
        """
        Вставка данных в таблицы квестов
        :param result:
        :param filename:
        :param time:
        :param time_mod:
        :param quest: Имя квеста (quest1, quest2 и т.д.)
        :param data: Словарь с данными (ключи: start_time, end_time, result)
        """
        query = f"""
                INSERT INTO {quest} (
                    first_quest_start_time,
                    result, 
                    description
                ) VALUES (?, ?, ?)
            """
        query2 = f"""
                INSERT INTO {quest} (
                    first_quest_final_time,
                    result, 
                    description
                ) VALUES (?, ?, ?)
            """

        with open(Path(__file__).parent.parent.parent.joinpath(filename), mode='r') as f:
            file_data = f.readlines()
            file_data_str = ''.join(file_data)

        # Вставляем данные в таблицу
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            if time_mod == 'first_quest_start_time':
                c.execute(query, (time, result, file_data_str))
            if time_mod == 'first_quest_final_time':
                c.execute(query2, (time, result, file_data_str))
            conn.commit()





class LoggerModel():

    # сделать метод для вывода в тг затем

    # main logger files
    standart_path: ClassVar[Path] = Path(__file__).parent.parent.parent.joinpath(
        "Info_Students/"
    )
    standart_path.mkdir(parents=True, exist_ok=True, mode=0o755)
    standart_path.joinpath("logger_standard.log").touch(exist_ok=True, mode=0o755)

    # files for user tries

    main_file_1: ClassVar[Path] = Path(__file__).parent.parent.parent.joinpath(
        "src/First_level/main"
    )
    main_file_2: ClassVar[Path] = Path(__file__).parent.parent.parent.joinpath(
        "src/Second_level/main"
    )
    main_file_3: ClassVar[Path] = Path(__file__).parent.parent.parent.joinpath(
        "src/Third_level/main"
    )
    main_file_4: ClassVar[Path] = Path(__file__).parent.parent.parent.joinpath(
        "src/Fourth_level/main"
    )

    # got data from user attempts
    stats: ClassVar[Path] = standart_path.joinpath("stats.sql")
    stats.touch(exist_ok=True, mode=0o755)
    # data = SQL_LOGGER_shema(stats)
