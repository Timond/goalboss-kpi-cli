#!/usr/bin/env python3
#Written by Tim Duncan @ Servers Australia 2019
import os

fileName = "kpis.txt"
mainMenu = ["Exit", "Summary", "New KPI"]
kpiList = []
kpiDictList = []
kpiMenu = ["Set Current Value", "Set Target Value", "Set Type", "Set Name", "Delete KPI", "Main Menu"]
kpiTypes = ["Total", "Percentage"]
loaded = False
fileData = None
currentSelection = None

def load_kpis():
    try:
        with open(fileName, "r") as f:
            fileData = f.read()
    except:
        print(f"{fileName} not found - creating now")
        with open(fileName, "w+") as f:
            pass
    if fileData:
        kpiList = fileData.split('\n')
        print("Loaded KPIs.")
        for k in kpiList:
            if k:
                kpiDict = new_kpi_dict(k)
                kpiDictList.append(kpiDict)
                add_kpi_to_menu(kpiDict)
    loaded = True

def print_menu(choiceList):
    c = 1
    for k in choiceList:
        item = f"{c}" + "."
        try:
            print(item, k["Name"])
        except:
            print(item, k)
        c += 1

def summary():
    os.system('clear')
    for k in kpiDictList:
        print_kpi(k)
    print("***********************")
    input("Press ENTER to continue")
    os.system('clear')

def print_kpi(kpi):
    if kpi:
        print("***********************")
        print("Name = ", kpi["Name"])
        print("Type = ", kpi["Type"])
        print("Current = ", kpi["Current"])
        print("Target = ", kpi["Target"])
        if kpi["Type"] == "p":
            percent = int(kpi["Current"]) / int(kpi["Target"]) * 100
            print("Percent = ", percent, "%")

def print_kpi_and_pause(kpi):
    if kpi:
        print_kpi(kpi)
        input("Press ENTER to continue")


def new_kpi_dict(kpi):
    if kpi:
        kpiName = kpi.split(',')[0]
        kpiType = kpi.split(',')[1]
        kpiCurrent = kpi.split(',')[2]
        kpiTarget = kpi.split(',')[3]
        kpiDict = { 
                "Name": kpiName,
                "Type": kpiType,
                "Current": kpiCurrent,
                "Target": kpiTarget
                }
        return kpiDict

def save_kpis():
    with open(fileName, "w+") as f:
        for k in kpiDictList:
            csvLine = str(k["Name"]) + "," + str(k["Type"]) + "," + str(k["Current"]) + "," + str(k["Target"]) + "\n"
            f.write(csvLine)

def add_kpi_to_menu(kpi):
    mainMenu.append(kpi)

def del_kpi(kpi):
    del mainMenu[mainMenu.index(kpi)]

def new_kpi():
    kpiName = input("Please enter KPI Name\n")
    kpiType = ""
    valid = False
    while not valid:
        print("Please select KPI type")
        print("Percentage = p")
        print("Total = t")
        kpiType = input()
        if kpiType == "p" or kpiType == "t":
            valid = True

    valid = False
    while not valid:
        try:
            kpiCurrent = int(input("Please set KPI current value\n"))
            kpiTarget = int(input("Please set the target\n"))
            valid = True
            kpiDict = { 
                "Name": kpiName,
                "Type": kpiType,
                "Current": kpiCurrent,
                "Target": kpiTarget
                }
            kpiDictList.append(kpiDict)
            return kpiDict
        except:
            print("Values must be integers")


def get_choice(choiceList):
    try:
        choice = int(input("Enter Choice:\n"))
        if (choice >= 0) and (choice <= len(choiceList)):
            print_choice(choiceList, choice)
            return choice
        else:
            raise Exception("Number not within range.")
    except:
        print("That's not a valid input, LeL. Try again.")

def edit_kpi(kpi):
    print_menu(kpiMenu)
    result = get_choice(kpiMenu)

def set_name(kpi):
    kpi["Name"] = input("Enter new KPI Name:\n")

def set_current_value(kpi):
    valid = False
    while not valid:
        try:
            kpi["Current"] = int(input("Enter new KPI Current Total:\n"))
            valid = True
        except:
            print("Please enter a valid integer")

def set_target_value(kpi):
    valid = False
    while not valid:
        try:
            kpi["Target"] = int(input("Enter new KPI Target Value:\n"))
            valid = True
        except:
            print("Please enter a valid integer")
        if kpi["Target"] == 0:
            print("Target cannot be 0. Please set a valid target")

def set_type(kpi):
    valid = False
    while not valid:
        kpi["Type"] = input("Enter new KPI Type (t for total, p for percentage):\n")
        if kpi["Type"] == "t" or kpi["Type"] == "p":
            valid = True
        else:
            print("Invalid Type. Please enter p for percentage or t for total")
    
def delete_kpi(kpi):
    global currentSelection
    currentSelection = None
    confirm = input("Are you sure you want to delete this KPI?")
    if confirm == "y" or confirm == "yes":
        i = kpiDictList.index(kpi)
        del kpiDictList[i]
        i = mainMenu.index(kpi)
        del mainMenu[i]

def print_choice(aList, i):
    try:
        print(f'You chose {aList[i - 1]["Name"]}')
    except:
        print(f'You chose {aList[i - 1]}')

def get_kpi(kpi):
    i = kpiDictList.index(kpi)
    return kpiDictList[i]

def main_menu():
    print_menu(mainMenu)
    result = get_choice(mainMenu)
    return result

def save_and_exit():
    try:
        print("Saving to", fileName)
        save_kpis()
    except:
        print("Something went wrong..")
        return 0
    quit()

def kpi_menu(kpi):
    global currentSelection
    os.system('clear')
    print_kpi(kpi)
    print("***********************")
    print_menu(kpiMenu)
    result = get_choice(kpiMenu)
    if result == 1:
        #Update Current Value
        set_current_value(kpi)
        print_kpi_and_pause(kpi)
        #main()
    elif result == 2:
        #Update Target Value
        set_target_value(kpi)
        print_kpi_and_pause(kpi)
        #main()
    elif result == 3:
        #Change type
        set_type(kpi)
        print_kpi_and_pause(kpi)
    elif result == 4:
        #Change name
        set_name(kpi)
        print_kpi_and_pause(kpi)
    elif result == 5:
        #Delete KPI from kpiMenu
        delete_kpi(kpi)
    else:
        currentSelection = None
        main()

def main():
    global loaded
    global currentSelection
    result = int()
    os.system('clear')
    print("*****SAU GOALBOSS KPI TRACKER*****")
    if not loaded:
        load_kpis()
        loaded = True
    if currentSelection == None:
        while not result:
            result = main_menu()
        if result == 1:
            save_and_exit()
        elif result == 2:
            os.system('clear')
            summary()
            main()
        elif result == 3:
            os.system('clear')
            newKpi = new_kpi()
            print_kpi(newKpi)
            input("New KPI Created. Press ENTER to continue")
            add_kpi_to_menu(newKpi)
            main()
        else:
            currentSelection = mainMenu[result - 1] 
            kpi_menu(currentSelection)
            main()
    else:
        kpi_menu(currentSelection)
        main()
main()
