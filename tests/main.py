from pathlib import Path
import pytest
from src.First_level import main
from only_dev_.models.model import KeyModel, KeyUpdater as k, MakePath
import re

variables = ["var", "egg", "foo", "bar", "spam", "ham"]


MakePath().create_path_if_not_exists(
    Path(__file__).parent.parent.joinpath("secrets/secret/very_secret")
)
KeyModel().init_json(
    Path(__file__).parent.parent.joinpath("secrets/secret/very_secret/secret_key.json")
)

first_module_update: list = ["P", "y", "t", "h", "o", "n"]


class TestModuleVariables:
    @pytest.mark.skipif(not all(hasattr(main, var) for var in variables),
                        reason="Some variables are missing in the main module")
    def test_variables1(self):
        for var in ["var", "egg", "spam", "foo", "bar", "ham"]:
            assert hasattr(main, var), f"Variable '{var}' does NOT exist in the module"
        k.change_key_value("first_key", "key1", "P")

    @pytest.mark.skipif(not all(hasattr(main, var) for var in variables),
                        reason="Some variables are missing in the main module")
    def test_print_output2(self, capfd):
        print(main.var + main.egg + main.foo + main.bar + main.spam + main.ham)
        out, err = capfd.readouterr()
        expected_output = "Python\n"
        assert out == expected_output, f"Expected '{expected_output}', but got '{out}'"
        k.change_key_value("first_key", "key2", "y")

    @pytest.mark.skipif(not hasattr(main, 'x') or not hasattr(main, 'y'),
                        reason="x or y are not defined in main module")
    def test_input_3(self):
        assert isinstance(main.x, (int, float)), "main.x must be int or float"
        assert isinstance(main.y, (int, float)), "main.y must be int or float"

        assert main.addition == main.x + main.y, "result of addition (+) is wrong"
        assert main.subtraction == main.x - main.y, "result of subtraction (-) is wrong"
        assert main.multiplication == main.x * main.y, "result of multiplication (*) is wrong"
        assert main.division == main.x // main.y, "result of division (//) is wrong"

    def test_comment_4(self):
        with open('../src/First_level/main.py', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line == re.search('^#I [*.] python$', line):
                    assert True
