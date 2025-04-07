
from typing import List
from core.api import Api
import os
import importlib
import pkgutil

WEBAPP_URL = os.getenv('WEBAPP_URL', 'http://localhost:5173')

ignore_folders = ['__pycache__', '_types']

def get_controller_paths(base_path: str, ignore_folders: str) -> List[str]:
    """This function gets all the paths of the controllers in the src/controller folder"""
    paths = []
    for root, dirs, _ in os.walk(base_path):
        for d in dirs:
            if d not in ignore_folders:
                paths.append(os.path.join(root, d))
    paths.append(base_path)
    return paths

def initialize_controllers():
    """
    Initializes and imports all controller modules from the specified controllers directory.

    This function constructs the path to the controllers directory, retrieves all controller paths,
    and iterates through them to import each module dynamically. It prints the name of each module
    being imported.

    Raises:
        ImportError: If there is an error importing a module.

    Note:
        The function assumes that the controllers are located in the 'src/controller' directory
        relative to the current file's directory.
    """
    controllers_path = os.path.join('src', 'controller')
    paths = get_controller_paths(
        os.path.join(os.path.dirname(__file__), controllers_path), ignore_folders
    )
    for importer, module_name, ispkg in pkgutil.iter_modules(paths):
        relative_path = os.path.relpath(importer.path, controllers_path)
        full_path = f'{controllers_path}{os.sep}{relative_path}'
        full_module_name = f'{full_path.replace(os.sep, '.')}.{module_name}'
        print(f'\033[92mImporting {full_module_name}\033[0m')
        if not ispkg:
            importlib.import_module(full_module_name)

initialize_controllers()

api_controller = Api()
app = Api.application

@app.after_request
def handle_options(response):
    response.headers['Access-Control-Allow-Origin'] = WEBAPP_URL
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'

    return response

app.run(debug=True)