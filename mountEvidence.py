import subprocess
import os
from pathlib import Path
import sys

def mountImage(mainReport, runner, file): # Mounts the evidence partitons
    loopDevice = runner.runCommand(f"losetup -Prf --show {file}")[0]
    cleanedLoopDevice = loopDevice.replace("\n", "")
    options = runner.runCommand(f"ls {cleanedLoopDevice}p*")[0].split("\n")

    for option in options:
        if option != "":
            number = option[-1]
            runner.runCommand(f"mkdir analysis{number}")
            runner.runCommand(f"mount {option} analysis{number}")

    return cleanedLoopDevice

def unMountImage(mainReport, runner, loopDevice): # Unmounts the evidence partions
    options = runner.runCommand(f"ls {loopDevice}p*")[0].split("\n")

    for option in options:
        if option != "":
            number = option[-1]
            runner.runCommand(f"umount analysis{number}")
            runner.runCommand(f"rm -rf analysis{number}")

    runner.runCommand(f"losetup -d {loopDevice}")