import os
import sys

def fileHashing(mainReport, runner, directory, outputDirectory): # Hashes all files in a dir and gets a hash list outputted elsewhere
    runner.runCommand(f"find {directory} -type f -exec sha256sum {{}} \\; > {outputDirectory}")

def recycleBin(mainReport, runner, number): # Tries to pull all items in the recylce bin of the drive
    if os.path.exists(f"./analysis{number}/$RECYCLE.BIN/"):
        runner.runCommand(f"mkdir RecyleBinA{number}")
        runner.runCommand(f"cp -r ./analysis{number}/\\$RECYCLE.BIN/ ./RecyleBinA{number}/")
        runner.runCommand(f"find ./RecyleBinA{number}/ -type f -exec sha256sum {{}} \\; > ./sha256Hashes/recylceScanAnalysis{number}.sha256sum")

def deletedFileRecovery(mainReport, runner, number, start, file): # Recovers all delted files
    runner.runCommand(f"mkdir -p ./deletedFileRecovery/mmls{number}/")        
    runner.runCommand(f"tsk_recover -o {start} -e {file} ./deletedFileRecovery/mmls{number}/")

def generateMmlsImageHTML(mainReport, runner, number): # Generates a HTML file that can be use to browse all images pulled from the deleted files
    runner.runCommand(f"""find ./deletedFileRecovery/mmls{number} -type f -print0 | xargs --null file -m ./magic.short | grep "_image_" | awk -F: '{{print "<p><a href=\\""$1"\\">" $1 "</a></p>"}}' > ./image_list.html""")