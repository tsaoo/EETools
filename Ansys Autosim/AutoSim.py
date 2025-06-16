from pyaedt import Maxwell2d
from pyaedt import Desktop
import os, sys, time
import csv
from datetime import datetime

sleepSlot = 10

outputDir = r'xxx\AutoSimResult'
planPath = r'xxx\AutoSimPlan.csv'
projectPath = r"xxx.aedt"

designName = 'xxx'
setupName = 'Setup1'
plotName = 'Winding Plot 1'

class DualLogger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding="utf-8")
        self._newline = True

    def write(self, message):
        lines = message.splitlines(keepends=True)
        for line in lines:
            if self._newline and line.strip() != "":
                timestamp = datetime.now().strftime("[%H:%M:%S]: ")
                line = timestamp + line
            self._newline = line.endswith('\n')
            self.terminal.write(line)
            self.log.write(line)
            self.log.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()

timeStamp = datetime.now().strftime("AutoSim_log_%Y-%m-%d_%H-%M-%S.txt")
sys.stdout = DualLogger(timeStamp)

with open(planPath, mode='r', newline='', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    simPlan = [dict(row) for row in reader]
print(f"{str(len(simPlan))} plans loaded from {planPath}.")

print("Initiating Ansys Desktop")
Desktop(specified_version="2024.2", non_graphical=True, new_desktop_session=False)
print("Ansys Desktop initiated")

print("Loading Maxwell 2D Project")
maxwell = Maxwell2d(projectname=projectPath, designname=designName)
print("Project loaded successfully")

simIndex = 1
for simSet in simPlan:
    print('Starting simulation [' + str(simIndex)+ '/' + str(len(simPlan)) + ']')
    for variableName in simSet:
        maxwell[variableName] = simSet[variableName]
        print('[' + variableName + '] <- ' + maxwell[variableName])
    
    print(f'Initiating {setupName}')
    maxwell.analyze_setup(name=setupName, cores=12, tasks=12)
    print(f'{setupName} finished')

    fileName = str(simIndex) + '.csv'
    print(f'Exporting result to {plotName}.csv')
    maxwell.post.export_report_to_csv(project_dir=outputDir, plot_name=plotName)
    print('Renaming as ' + fileName)
    os.rename(f'{outputDir}\{plotName}.csv', f'{outputDir}\{fileName}')
    print("Result saved successfully")
    
    print('Saving Maxwell project')
    maxwell.save_project()
    print('Project saved successfully')

    time.sleep(sleepSlot)
    simIndex = simIndex + 1
    
print('AutoSim finished, releasing Ansys Desktop')
maxwell.release_desktop(close_projects=True, close_desktop=True)
print('Ansys Desktop released, AutoSim terminated')