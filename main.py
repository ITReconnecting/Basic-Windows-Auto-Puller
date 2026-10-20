import subprocess
import os
import argparse
from pathlib import Path
import sys

from report import Report
from imageStructure import getImageStructure
from mountEvidence import mountImage, unMountImage
from runcommand import Runner
from evidenceAnalysis import fileHashing, recycleBin, deletedFileRecovery, generateMmlsImageHTML

def main():
    parser = argparse.ArgumentParser(description="Windows System Information Puller")

    parser.add_argument("path", default=argparse.SUPPRESS, nargs="?")

    args = parser.parse_args()

    file = Path(args.path)

    if not os.path.exists(file): # Ensures File Exists
        print("File does not exist")
        exit()

    mainReport = Report() # Starts the report class
    runner = Runner(mainReport) # Sets up the command running class

    mainReport.addLine("--- SHA256 Hash ---") # Gets a Hash of the raw image
    mainReport.addLine(runner.runCommand(f"sha256sum {file}")[0])

    runner.runCommand(f"mkdir sha256Hashes")

    mmlsImportant = getImageStructure(mainReport, runner, file) # Pulls all the image data

    loopDevice = mountImage(mainReport, runner, file) # Mounts the partitions on a loop device

    mainReport.addLine(f"--- Partitions Mounted ---")

    evidenceDirectories = runner.runCommand("ls | grep analysis")[0].split("\n") # Gets all analysis directories

    mainReport.addLine(f"--- SHA256 File List for analysis mount points ---") # Gets a list of all files in each analysis directory and there sha256 hash values

    for directory in evidenceDirectories:
        if directory != "":
            number = directory[-1].strip()
            fileHashing(mainReport, runner, directory, f"./sha256Hashes/scanAnalysis{number}.sha256sum")
            numLines = sum(1 for _ in open(f'./sha256Hashes/scanAnalysis{number}.sha256sum'))
            mainReport.addLine(f"Number of hashes pulled from analysis{number} >> {numLines}")
            if numLines > 0:
                recycleBin(mainReport, runner, number)
                recylceNumLines = sum(1 for _ in open(f'./sha256Hashes/recylceScanAnalysis{number}.sha256sum'))
                if recylceNumLines > 0:
                    mainReport.addLine(f"Number of files pulled from analysis{number}'s recycle bin >> {recylceNumLines}")

    unMountImage(mainReport, runner, loopDevice) # Unmounts the partitions 

    mainReport.addLine(f"--- Paritions Unmounted ---")

    mainReport.addLine(f"--- Deleted File Recovery ---") # Recovers all deleted files

    for part in mmlsImportant:
        deletedFileRecovery(mainReport, runner, part[0], part[1], file)
        fileHashing(mainReport, runner, f"./deletedFileRecovery/mmls{part[0]}/", f'./sha256Hashes/deletedFileRecovery{part[0]}.sha256sum')
        numLines = sum(1 for _ in open(f'./sha256Hashes/deletedFileRecovery{part[0]}.sha256sum'))
        mainReport.addLine(f"Number of deleted files recovered from mmls partiton {part[0]} >> {numLines}")
        generateMmlsImageHTML(mainReport, runner, part[0])
        mainReport.addLine("html index file created of all deleted images")

    mainReport.writeReport() # Writes up the main reports

if __name__ == "__main__":
    main()