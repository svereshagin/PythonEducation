from pathlib import Path

project_root = Path(__file__).parent.parent.parent
project_src = project_root / 'src'
module_names = ["First_level/", "Second_level/", "Third_level/", "Fourth_level/"]
project_files_for_test = {
    "main_1": project_src.joinpath(module_names[0] + "main1.py"),
    "main_2": project_src.joinpath(module_names[1] + "main2.py"),
    "main_3": project_src.joinpath(module_names[2] + "main3.py"),
    "main_4": project_src.joinpath(module_names[3] + "main4.py"),
}

sql_database_path = project_root / 'sql_database'
sql_database_file =sql_database_path.joinpath('database_db.sql')
