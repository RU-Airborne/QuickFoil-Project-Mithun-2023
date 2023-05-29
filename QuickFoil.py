from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill
from aerosandbox import XFoil, Airfoil
import numpy as np
import pandas as pd
from pyfiglet import Figlet

def get_airfoils():
    airfoils = []
    while True:
        try:
            request = input("Airfoil: ")
            if request.lower() == 'done':
                if len(airfoils) < 2:
                    raise ValueError
                return airfoils
            airfoils.append((request, Airfoil(name=request).repanel(150)))
        except TypeError:
            print("Invalid Airfoil! (Not a NACA 4 Digit or in UIUC Database)")
        except ValueError:
            print("Please input at least two airfoils")

def get_Re():
    while True:
        try:
            Re = float(input("Re: "))
            if Re <= 0:
                raise ValueError
            return Re
        except ValueError:
            print("Invalid Reynolds Number")
            continue

def get_Mach():
    while True:
        try:
            Mach = float(input("Mach: "))
            if 0 < Mach <= 0.3:
                return Mach
            else:
                raise ValueError    
        except ValueError:
            print("Invalid Mach Number")
            continue

def get_alphas():
    while True:
        try:
            alpha_first = int(input("First Alpha:  "))
            alpha_last = int(input("Last Alpha: "))
            alpha_increment = float(input("Alpha Increment: "))
            if alpha_last < alpha_first or alpha_increment < 0:
                raise ValueError

            alphas = np.arange(alpha_first, alpha_last + 1, alpha_increment)            
            return alphas
        except ValueError:
            print("Invalid Angle of Attack Range")
            continue

def get_optimizer():
    while True:
        optimizer = input("Optimize for: ").upper()
        if optimizer in ['CL', 'CD', 'CDP', 'CL/CD', 'CM', 'CPMIN']:
            return optimizer
        
def get_fileName():
    FileName = input("File Name: ")
    if '.' not in FileName:
        return FileName

def run_XFoil(airfoil, re, mach, alphas):  
        xf = XFoil(
        airfoil=airfoil.repanel(n_points_per_side=200),
        Re = re,
        mach=mach,
        max_iter=1000,
        timeout=60,
        )

        return xf.alpha(alphas)

def write_excel(airfoils, data, file_name='SimpFoil_Run',optimizer='CL'):
    """
    CHANGE FILE PATH HERE. LEAVE \{file_name}.xlsx AND CHANGE EVERYTHING ELSE
    """
    file_path = fr'C:\Users\reach\Desktop\2D_Airfoil_Easy_Anaysis_Project\Quick-and-Easy-2D-Airfoil-Analysis\Excel_Data\{file_name}.xlsx'
    workbook = Workbook()
    writer = pd.ExcelWriter(path=file_path, engine='openpyxl')
    
    dataFrame_list = []

    match optimizer:
        case 'CL' | 'CL/CD':
            reverse_sort = True
        case 'CD' | 'CDP' | 'CM' | 'CPMIN':
            reverse_sort = False

    for i in range(len(data[0]['alpha'])):
        writing_data = []
        for j, airfoil in enumerate(data):
            writing_data.append({
                "Airfoil": airfoils[j][0],
                "CL": airfoil['CL'][i],
                "CD": airfoil['CD'][i],
                "CDp": airfoil['CDp'][i],
                "CL/CD": airfoil['CL'][i]/airfoil['CD'][i],
                "CM": airfoil['CM'][i],
                "Cpmin": airfoil['Cpmin'][i],
                "Top_Xtr": airfoil['Top_Xtr'][i],
                "Bot_Xtr": airfoil['Bot_Xtr'][i]
            })
        
        dataFrame_list.append(pd.DataFrame(sorted(writing_data, key=lambda s: s[optimizer],reverse=reverse_sort)))

    
    alphas = [int(n) for n in np.ndarray.tolist(data[0]['alpha'])]

    for i, df in enumerate(dataFrame_list):
        df.to_excel(writer, index=False, header=True, sheet_name=f"Alpha(deg)={alphas[i]}")
        

    writer.close()


def main():
    figlet = Figlet()
    figlet.setFont(font='doom')
    print(figlet.renderText("Welcome to QuickFoil !"))

    print("Enter the desired airfoils and type 'done' when finished")
    airfoils = get_airfoils()
    print()

    print("Enter the desired Reynolds number")
    Re = get_Re()
    print()

    print("Enter the desired Mach number")
    Mach = get_Mach()
    print()

    print("Enter the desired range of angle of attacks")
    alphas = get_alphas()
    print()

    Optimizer = get_optimizer()
    print()

    print("Enter the desired file name")
    FileName = get_fileName()

    data = []
    for airfoil in airfoils :  
        data.append(run_XFoil(airfoil[1], Re, Mach, alphas))

    write_excel(airfoils, data, file_name=FileName, optimizer=Optimizer)

    print(figlet.renderText("Success !"))

if __name__ == '__main__':
    main()