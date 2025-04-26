import os

import importlib.util
from typing import Callable
import argparse
import dotenv

# Initialize the environment variables
dotenv.load_dotenv(override=True)

script_mapping = dict[str, dict[str, Callable]]

def load_script_mapping(directory: str) -> script_mapping:
    script_map = script_mapping()
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            if dir_name == "scripts":
                script_path = os.path.join(root, dir_name)
                for script_file in os.listdir(script_path):
                    if script_file.endswith(".py"):
                        script_file_path = os.path.join(script_path, script_file)
                        spec = importlib.util.spec_from_file_location(script_file, script_file_path)
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        if hasattr(module, 'execute') and callable(getattr(module, 'execute')):
                            file_name = os.path.splitext(os.path.basename(script_file_path))[0]
                            script_directory_path = os.path.relpath(os.path.dirname(script_file_path), directory)
                            directory_path = os.path.dirname(script_directory_path)
                            if directory_path not in script_map:
                                script_map[directory_path] = {}
                            script_map[directory_path][file_name] = getattr(module, 'execute')

    return script_map

if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    script_map = load_script_mapping(script_directory)

    parser = argparse.ArgumentParser(description="Run a script from the script mapping.")
    parser.add_argument("path_name", type=str, help="The path name where the script is located.")
    parser.add_argument("file_name", type=str, help="The file name of the script to run.")
    parser.add_argument("additional_args", nargs=argparse.REMAINDER, help="Additional arguments to pass to the script.")
    args = parser.parse_args()

    path_name = args.path_name
    file_name = args.file_name
    kwargs = args.additional_args
    
    kwargs = {}
    for arg in args.additional_args:
        try:
            key, value = arg.split('=', 1)
        except ValueError:
            raise ValueError(f"Argument '{arg}' does not follow the pattern 'key=value'")
        kwargs[key] = value

    if path_name in script_map and file_name in script_map[path_name]:
        script_map[path_name][file_name](**kwargs)
    else:
        print(f"Script {file_name} not found in path {path_name}")