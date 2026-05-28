import os
import subprocess

COMMAND = "cls" if os.name == "nt" else "clear"


def clear():
    subprocess.run([COMMAND], shell=True)
