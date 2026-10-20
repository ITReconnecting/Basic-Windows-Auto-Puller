import subprocess

class Runner():

    def __init__(self, report):
        self.report = report

    def runCommand(self, command): # Runs the command
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.wait()
        self.report.addHistory(command)
        return (output.decode("utf-8"), err)