import subprocess
import os
from pathlib import Path
import sys

def getImageStructure(mainReport, runner, file): # Coallates all the information on the image file
    fdiskResults = fdisk(runner, file)
    gpt = fdiskResults[1]

    if not gpt: # Uses fdisk for non gpt images
        mainReport.addLine("--- fdisk output ---")
        for line in fdiskResults[0]:
            mainReport.addLine(line)

    if gpt: # Uses gdisk for gpt images
        gdiskResults = gdisk(runner, file)
        mainReport.addLine("--- gdisk output ---")
        for line in gdiskResults:
            mainReport.addLine(line)
    
    importantLable = "Basic data partition"
    importantMmls = []

    mmlsResult = mmls(runner, file)
    mainReport.addLine("--- mmmls output ---")
    for line in mmlsResult:
        mainReport.addLine(line)
        if importantLable in line:
            splitLine = line.split(" ")
            splitLine = list(filter(('').__ne__, splitLine))
            importantMmls.append((splitLine[1], splitLine[2], splitLine[3]))
            importantMmls = list(dict.fromkeys(importantMmls))

    return importantMmls


def fdisk(runner, file): # Runs and processes fdisk
    gpt = False
    result = []

    fdiskResponse = runner.runCommand(f"fdisk -l {file}")
    fdiskList = fdiskResponse[0].split("\n") # Gets the fdisk output

    if fdiskList[4].split(" ")[-1] == "gpt":
        gpt = True
        return (None, gpt)

    sectorSize = fdiskList[2]
    identifier = fdiskList[5]

    partitions = []

    result.append(identifier)
    result.append(sectorSize)
    result.append('')
    for line in partitions:
        result.append(line)
        

    return (result, gpt)

def gdisk(runner, file): # Runs and processes gdisk
    gdiskResponse = runner.runCommand(f"gdisk -l {file}")
    gdiskList = gdiskResponse[0].split("\n")

    result = []

    guid = gdiskList[11]
    sectorSize = gdiskList[10]
    
    partitions = []

    for x in range(18, len(gdiskList)):
        partitions.append(gdiskList[x])

    result.append(guid)
    result.append(sectorSize)
    result.append('')
    for line in partitions:
        result.append(line)

    return result

def mmls(runner, file): # Runs and processes mmls

    mmlsResponse = runner.runCommand(f"mmls {file}")
    mmlsList = mmlsResponse[0].split("\n")

    result = []
    
    for x in range(4, len(mmlsList)):
        result.append(mmlsList[x])

    return result