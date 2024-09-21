from pathlib import Path

path_to_root = Path(__file__).parent
secret_directories = path_to_root.joinpath("secrets/secret/very_secret")
secret_file = secret_directories.joinpath("secret_key.json")
first_module_update: list = ['P', 'y', 't', 'h', 'o', 'n']

