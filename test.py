from pathlib import Path
from pprint import pprint
import subprocess
import os
import sys

path = Path(Path.cwd().parent, "Kitleman", "main.py")
venv_path = Path(Path.cwd().parent, "Kitleman", "venv", "Scripts")

command_ls = []

command_ls.append(
        f"start cmd /k cd /d {venv_path} & activate & cd /d {path.parent} & {path}"
    )
    #  
# print(command_ls)
# for command in command_ls:
#     print(command.split())
#     subprocess.run(command.split(), shell=True)

if __name__ == '__main__':
    a = f"start cmd /k {path}"
    # subprocess.call(a, shell=True)
    # subprocess.Popen(f"start cmd /k cd /d {venv_path} & active".split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    os.system(f"cd /d {venv_path} & activate & cd /d {path.parent} & {path}")
    # sys.exit(0)
    pass