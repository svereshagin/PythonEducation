import pytest
from src.First_level import main
from only_dev_.models.model import TestFileCreateModel
import re

variables = ["var", "egg", "foo", "bar", "spam", "ham"]


file = TestFileCreateModel()
file.init_json()


first_module_update: list = ["P", "y", "t", "h", "o", "n"]


class TestModuleVariables:
    @pytest.mark.skipif(not all(hasattr(main, var) for var in variables),
                        reason="Some variables are missing in the main module")
    def test_variables1(self):
        for var in variables:
            assert hasattr(main, var), f"Variable '{var}' does NOT exist in the module"
            file.change_test_result(module='first_key', test_n='test1')

    @pytest.mark.skipif(not all(hasattr(main, var) for var in variables),
                        reason="Some variables are missing in the main module")
    def test_print_output2(self, capfd):
        print(main.var + main.egg + main.foo + main.bar + main.spam + main.ham)
        out, err = capfd.readouterr()
        expected_output = "Python\n"
        assert out == expected_output, f"Expected '{expected_output}', but got '{out}'"
        file.change_test_result(module='first_key', test_n='test2')

    @pytest.mark.skipif(not hasattr(main, 'x') or not hasattr(main, 'y'),
                        reason="x or y are not defined in main module")
    def test_input_3(self):
        assert isinstance(main.x, (int, float)), "main.x must be int or float"
        assert isinstance(main.y, (int, float)), "main.y must be int or float"

        assert main.addition == main.x + main.y, "result of addition (+) is wrong"
        assert main.subtraction == main.x - main.y, "result of subtraction (-) is wrong"
        assert main.multiplication == main.x * main.y, "result of multiplication (*) is wrong"
        assert main.division == main.x // main.y, "result of division (//) is wrong"
        file.change_test_result(module='first_key', test_n='test3')

    def test_comment_4(self):
        with open('../src/First_level/main.py', 'r') as f:
            lines = f.readlines()
            found = False
            for line in lines:
                if re.search(r'^#I love python$', line):
                    found = True
                    break
            assert found, "'#I love python' comment not found"
            file.change_test_result(module='first_key', test_n='test4')
    def test_5(self):
        OK = True
        assert OK == True
        file.change_test_result(module='first_key', test_n='test5')
        # file.generate_hash_value(module='first_key')
        file.check_all_module_tests('first_key')
        file.generate_hash_value('first_key', exp=11)

    # def test_comment_5(self):
    #     with open('../src/First_level/fourth_key.md', 'r') as f:
    #         lines = f.readlines()
    #         found = False
    #         for line in lines:
    #             if re.search(r'hash', line):
    #                 found = True
    #                 break
    #
    #         # Убедитесь, что нашли строку с "hash"
    #         assert found, "'hash' not found in fourth_key.md"
