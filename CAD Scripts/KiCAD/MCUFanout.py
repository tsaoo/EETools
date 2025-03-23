import csv
import sexpdata
import skip as sk
import tkinter as tk
from tkinter import ttk

UnitSpace = 1.27        # KiCad recommends a 50mil grid for all schematics

SchPath = ''
CsvPath = ''
EnableGlobal = True
EnableLocal = True
FanOutLength = 10
ComponentKeyType = 0
ComponentKey = ''

PinDictionary = {}

def ReadPinOutCsv(path):
    pinDictionary = {}
    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            designator = row[0].strip()
            function = row[3].strip()
            pinDictionary[designator] = function
    return pinDictionary

def LocateMcuByPrefix(sch:sk.Schematic, prefix:str):
    compList = []
    symbols = sch.symbol
    for comp in symbols:
        if comp.property.Value.value[:len(prefix)] == prefix:
            compList.append(comp)
    return compList

def LocateMcuByReference(sch:sk.Schematic, ref:str):
    return sch.symbol.reference_matches(ref)

def FanOutMCU(sch:sk.Schematic, comp:sk.Symbol, length:int, pinLib:dict):
    compPins = comp.pin
    for pin in compPins:
        if not pinLib[pin.value]: continue
        pinFunc = pinLib[pin.value]

        fanOutDirection = -1 if pin.location.value[2] == 0 else 1
        fanOutWire = sch.wire.new()
        fanOutWire.start_at(pin)
        fanOutWire.delta_y = 0
        fanOutWire.delta_x = length * UnitSpace * fanOutDirection

        if EnableGlobal:
            fanOutLabel = sch.global_label.new()
            fanOutLabel.move(fanOutWire.end.value[0], fanOutWire.end.value[1], pin.location.value[2])
            fanOutLabel.effects.justify.value = 'right' if pin.location.value[2] == 0 else 'left'
            fanOutLabel.value = pinFunc
        
        if EnableLocal:
            fanOutLabel = sch.label.new()
            fanOutLabel.move(fanOutWire.end.value[0], fanOutWire.end.value[1], pin.location.value[2])
            fanOutLabel.effects.justify.value = sexpdata.parse('left bottom') if pin.location.value[2] == 0 else sexpdata.parse('right bottom')
            fanOutLabel.value = pinFunc
    return


def Main():
    root = tk.Tk()
    root.title("MCUFanout")
    root.geometry("400x250") 

    schPathInput = tk.StringVar()
    csvPathInput = tk.StringVar()
    fanOutLengthInput = tk.StringVar()
    componentKeyInput = tk.StringVar()
    enableGlobalInput = tk.BooleanVar()
    enableLocalInput = tk.BooleanVar()

    label_sch = ttk.Label(root, text="Sch File Path: ")
    label_sch.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    textbox_sch = ttk.Entry(root, textvariable=schPathInput, width=40)
    # textbox_sch.insert(0, _schpath) 
    textbox_sch.grid(row=0, column=1, padx=10, pady=5)

    label_csv = ttk.Label(root, text="Pinout File Path: ")
    label_csv.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    textbox_csv = ttk.Entry(root, textvariable=csvPathInput, width=40)
    # textbox_csv.insert(0, _csvpath)
    textbox_csv.grid(row=1, column=1, padx=10, pady=5)

    label_fanout = ttk.Label(root, text="Fanout Length: ")
    label_fanout.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    textbox_fanout = ttk.Entry(root, textvariable=fanOutLengthInput, width=40)
    textbox_fanout.insert(0, '10')
    textbox_fanout.grid(row=2, column=1, padx=10, pady=5)

    label_key_type = ttk.Label(root, text="Component Key: ")
    label_key_type.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    combobox_key_type = ttk.Combobox(root, values=["Reference", "Value Prefix"], state="readonly", width=15)
    combobox_key_type.grid(row=3, column=1, padx=10, pady=5)
    combobox_key_type.current(1)

    textbox_component_key = ttk.Entry(root, textvariable=componentKeyInput, width=40)
    textbox_component_key.insert(0, 'STM32')
    textbox_component_key.grid(row=4, column=1, padx=10, pady=5)

    checkbox_global = ttk.Checkbutton(root, text="Enable Global Label", variable=enableGlobalInput)
    checkbox_global.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    checkbox_local = ttk.Checkbutton(root, text="Enable Local Label", variable=enableLocalInput)
    checkbox_local.grid(row=5, column=1, padx=10, pady=5, sticky="w")
    
    def run_action():
        global SchPath, CsvPath, EnableGlobal, EnableLocal, FanOutLength, ComponentKey, ComponentKeyType
        SchPath = schPathInput.get()
        CsvPath = csvPathInput.get()
        EnableGlobal = enableGlobalInput.get()
        EnableLocal = enableLocalInput.get()
        FanOutLength = int(fanOutLengthInput.get())
        ComponentKey = componentKeyInput.get()
        ComponentKeyType = combobox_key_type.current()
        root.quit()

    button_run = ttk.Button(root, text="Run", command=run_action)
    button_run.grid(row=6, column=0, columnspan=2, pady=10)

    root.columnconfigure(1, weight=1)
    root.mainloop()

    sch = sk.Schematic(SchPath)
    PinDictionary = ReadPinOutCsv(CsvPath)

    if ComponentKeyType == 0:
        compList = LocateMcuByReference(sch, ComponentKey)
    else:
        compList = LocateMcuByPrefix(sch, ComponentKey)
    
    for comp in compList:
        FanOutMCU(sch, comp, FanOutLength, PinDictionary)

    sch.write(SchPath)
    return

if __name__ == "__main__":
    Main()