from datetime import datetime

class Report():

    def __init__(self):
        self.lines = []
        self.commandHistory = []

        start = f"Program Started: {datetime.now().strftime("%d/%m/%Y")} at {datetime.now().strftime("%H:%M")}"
        self.lines.append(start)
        self.commandHistory.append(start)
        

    def addLine(self, item):
        self.lines.append(item)

    def addHistory(self, item):
        self.commandHistory.append(item)

    def writeReport(self):
        end = f"Program Ended: {datetime.now().strftime("%d/%m/%Y")} at {datetime.now().strftime("%H:%M")}"
        self.lines.append(end)
        self.commandHistory.append(end)

        f = open("report.txt", "w")
        for line in self.lines:
            f.write(line)
            f.write("\n")
        f.close()

        f = open("commandHistory.txt", "w")
        for command in self.commandHistory:
            f.write(command)
            f.write("\n")
        f.close()