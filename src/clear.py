import os
import subprocess

COMMAND = "cls" if os.name == "nt" else "clear"


def clear():
    subprocess.run([COMMAND], shell=True)
    # Esta es la versión moderna del obsoleto clásico os.system(COMMAND)
