import pytest
from only_dev_.models.model import TestFileCreateModel, SQL_LOGGER_shema, PreCreatingProjectFiles
import re
from src.First_level import main1



variables = ["var", "egg", "foo", "bar", "spam", "ham"]
PreCreatingProjectFiles.create_project_files()
file = TestFileCreateModel()
log = SQL_LOGGER_shema()
file.init_json()

previsious_test = False


first_module_update: list = ["P", "y", "t", "h", "o", "n"]


class TestModuleVariables:
    @pytest.mark.skipif(not all(hasattr(main1, var) for var in variables),
                        reason="Some variables are missing in the main module")
    def test_variables1(self):
        global previsious_test
        for var in variables:
            assert hasattr(main1, var), f"Variable '{var}' does NOT exist in the module"
            file.change_test_result(module='first_key', test_n='test1')

    @pytest.mark.skipif(not all(hasattr(main1, var) for var in variables or previsious_test==False),
                        reason="Some variables are missing in the main module")
    def test_print_output2(self, capfd):
        print(main1.var + main1.egg + main1.foo + main1.bar + main1.spam + main1.ham)
        out, err = capfd.readouterr()
        expected_output = "Python\n"
        assert out == expected_output, f"Expected '{expected_output}', but got '{out}'"
        file.change_test_result(module='first_key', test_n='test2')

    @pytest.mark.skipif(not hasattr(main1, 'x') or not hasattr(main1, 'y'),
                        reason="x or y are not defined in main module")
    def test_input_3(self):
        assert isinstance(main1.x, (int, float)), "main.x must be int or float"
        assert isinstance(main1.y, (int, float)), "main.y must be int or float"

        assert main1.addition == main1.x + main1.y, "result of addition (+) is wrong"
        assert main1.subtraction == main1.x - main1.y, "result of subtraction (-) is wrong"
        assert main1.multiplication == main1.x * main1.y, "result of multiplication (*) is wrong"
        assert main1.division == main1.x // main1.y, "result of division (//) is wrong"
        file.change_test_result(module='first_key', test_n='test3')


    def test_comment_4(self):
        with open('../src/First_level/main1.py', 'r') as f:
            lines = f.readlines()
            found = False
            for line in lines:
                if re.search(r'^#I love python$', line):
                    found = True
                    break
            assert found, "'#I love python' comment not found"
            file.change_test_result(module='first_key', test_n='test4')
            file.generate_hash_value('first_key', 11)

    def test_comment_5(self):
        with open('../src/First_level/first_key.md', 'r') as f:
            lines = f.readlines()
            found = False
            for line in lines:
                if line != '':
                    found = True
                    break
        assert found, "'hash' not found in fourth_key.md"