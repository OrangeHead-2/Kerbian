import shutil
import os

def init_project(path):
    templates_dir = os.path.join(os.path.dirname(__file__), '../../../templates/project')
    if os.path.exists(path):
        raise FileExistsError(f"Directory {path} already exists.")
    shutil.copytree(templates_dir, path)
    print(f"Kerbian project initialized at {path}")