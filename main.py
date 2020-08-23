from pprint import pprint
from pathlib import Path
import subprocess
import signal
import json
import eel
import os

global script

_version = "0.0.1"

config_file = Path("config.json")

current_project_name = Path(Path.cwd())

def load_json(file):
    with open(file, "r", encoding="utf8") as json_file:
        data = json.load(json_file)

    return data

def export_json(file, data):
    with open(file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file)

def filter_directory(path):
    if path.is_dir() and (path != current_project_name):
        return True
    return False

def map_py_file(path):
    ls = []
    for inner_path in path.iterdir():
        if (inner_path.is_file() and
                inner_path.suffix == ".py" and
                not inner_path.name.replace(".py", "") in data["ignore_file_ls"]):

            ls.append(inner_path.name)

    return ls

def map_venv_status(path):
    for inner_path in path.iterdir():
        if inner_path.is_dir() and inner_path.name == data["venv_name"]:
            return True
    return False

def get_project_info():
    current_project_name = Path(Path.cwd())

    project_ls = list(
            filter(
                filter_directory,
                Path(data["project_directory"]).iterdir()
            )
        )

    project_file_ls = list(
        map(
            map_py_file,
            project_ls
        )
    )

    venv_status_ls = list(
        map(
            map_venv_status,
            project_ls
        )
    )
    
    dc = {}

    for i in range(len(project_ls)):
        project = project_ls[i]
        file_ls = project_file_ls[i]
        venv_status = venv_status_ls[i]
        dc[project.name] = {
            "file_ls": file_ls,
            "venv_status": venv_status
        }
    
    return dc

@eel.expose
def get_data():
    dc = {
        "project": get_project_info(),
        "title": "Project Center"
    }

    return dc 

@eel.expose
def run_script(id, file, venv):
    global script, running_script_name

    try:        
        if not script.poll(): # running
            if running_script_name != f"{id}\\{file}":
                eel.show_message(f"請先關閉{running_script_name}")
                return
            

            subprocess.call(['taskkill', '/F', '/T', '/PID',  str(script.pid)])

            return False

    except Exception as e:
        print(e)

    path = Path(data["project_directory"], id, file)

    if venv:
        venv_path = Path(data["project_directory"], id, data["venv_name"], "Scripts")

        command = f"cmd /k cd /d {venv_path} & activate & cd /d {path.parent} & {path}"
    else:
        command = f"cmd /k cd /d {path.parent} & {path}"

    script = subprocess.Popen(command, shell=False)
    running_script_name = f"{id}\\{file}"

    return True

if __name__ == "__main__":   
    data = load_json(config_file)

    eel.init("web")
    eel.start("index.html", size=(1100, 600))
