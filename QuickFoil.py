from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill
from aerosandbox import XFoil, Airfoil
import numpy as np
import pandas as pd
from typing import List
from tqdm import tqdm


class QuickFoil:
    def __init__(self, airfoils: List[str], Re: float = 100000, Mach: float = 0, alphas: np.ndarray = np.arange(-5, 15, 0.25), sort_by: str = "CL") -> None:
        self.airfoils = airfoils
        if Re <= 0:
            raise ValueError("Reynolds number must be greater than 0")
        if (Mach > 0.3) or (Mach < 0):
            raise ValueError("Mach number must be 0 <= Mach <= 0.3")

        self.Re = Re
        self.Mach = Mach
        self.alphas = alphas
        self.sort_by = sort_by

    def run_xfoil(self) -> List:
        data = []
        progress = tqdm(self.airfoils)
        for airfoil in progress:
            progress.set_postfix_str(airfoil) # displays a progress bar with name of current airfoil
            # print(f"Now running {airfoil}...")
            xf_airfoil = Airfoil(name=airfoil)
            xf = XFoil(
                airfoil=xf_airfoil.repanel(n_points_per_side=200),
                Re = self.Re,
                mach=self.Mach,
                max_iter=1000,
                timeout=60,)
            result = xf.alpha(self.alphas)
            data.append(result)
            # print(f"Finished {airfoil}")
        self.data = data
        return data

    def write_excel(self, file_name='SimpFoil_Run') -> None:
        """
        CHANGE FILE PATH HERE. LEAVE \{file_name}.xlsx AND CHANGE EVERYTHING ELSE
        """
        
        file_path = fr'./{file_name}.xlsx'
        # workbook = Workbook()
        writer = pd.ExcelWriter(path=file_path, engine='openpyxl')
        dataFrame_list = []
        if self.sort_by in ["CL", "CL/CD"]:
            reverse_sort = True
        elif self.sort_by in ['CD', 'CDp', 'CM', 'Cpmin']:
            reverse_sort = False

        for i in range(len(self.data[0]['alpha'])):
            writing_data = []
            for j, airfoil in enumerate(self.data):
                writing_data.append({
                    "Airfoil": self.airfoils[j],
                    "CL": airfoil['CL'][i],
                    "CD": airfoil['CD'][i],
                    "CDp": airfoil['CDp'][i],
                    "CL/CD": airfoil['CL'][i]/airfoil['CD'][i],
                    "CM": airfoil['CM'][i],
                    "Cpmin": airfoil['Cpmin'][i],
                    "Top_Xtr": airfoil['Top_Xtr'][i],
                    "Bot_Xtr": airfoil['Bot_Xtr'][i]
                })
            
            dataFrame_list.append(pd.DataFrame(sorted(writing_data, key=lambda s: s[self.sort_by],reverse=reverse_sort)))

        
        alphas = [int(n) for n in np.ndarray.tolist(self.data[0]['alpha'])]

        for i, df in enumerate(dataFrame_list):
            df.to_excel(writer, index=False, header=True, sheet_name=f"Alpha(deg)={alphas[i]}")
        writer.close()

def main():
    airfoils = [
        "naca6409",
        "naca4412", 
        "sa7038",
        ]
        # "naca4415",
        # "naca2410",
        # "naca2410",
        # "naca2408",
        # "naca4424",
        # "naca2414",
        # "naca2415",
        # "naca1408",
        # "naca1410",
        # "naca1412",]
    
    Re = 350000
    Mach = 0.05
    alphas = np.arange(-2, 2, 1)
    sort_by = "CL"
    fileName = 'SampleQuickFoilRun'
    qf = QuickFoil(airfoils, Re=Re, Mach=Mach, alphas=alphas, sort_by=sort_by)

    data = qf.run_xfoil()
   
    qf.write_excel(file_name=fileName)

if __name__ == '__main__':
    main()