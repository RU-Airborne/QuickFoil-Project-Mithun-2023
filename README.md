# Quick XFoil (QuickFoil) Project by Mithun Krishnan
 Welcome to quick XFoil, otherwise known as QuickFoil! (working title?)

 This is an extremely early version of QuickFoil. There are a lot of bugs I definitely left in and invalid inputs the user might type that need to be accounted for. A lot of code cleanup can already be done, but this version works if everything is inputted well. This is a personal project for me to (1) learn Python and (2) aid Rutgers AIAA's Design, Build, Fly team, RU Airborne, in the design of the competition aircraft. The end goal of this project is to make it user-friendly and replace the terminal command approach with a GUI. There is a picture of my vision of the GUI in the repo available. 

 The gist of the project is to take in however many airfoils as the user pleases and run a simple, viscous, incompressible, 2D, low Mach, and low Reynolds number XFoil simulation. Once completed, the program will spit out an Excel file with all the data. Each sheet in the Excel workbook will represent the various angles of attack the user has requested. The user can 'optimize' a specific aerodynamic parameter the simulation solves. For example, suppose the user wants to optimize their airfoils for lift. In that case, the data will be sorted by decreasing lift coefficient. Similarly, if the user wants to minimize drag, the data will be sorted by increasing the drag coefficient. Hence, instead of running an XFLR5 simulation for each airfoil and manually inputting data into an Excel sheet, this program does everything for you AND sorts to the user's wishes. A comparison of this process is found in the repo with description "QuickFoilComparison", where QuickFoil was run on some of the airfoils from 2022 analysis optimizing for Cl/Cd. The hero that can make this program possible is the aerosandbox Python library, which provides the ability to call XFoil through Python code (shoutout to Noah McAllister for discovering it and an even more significant shoutout to the people who made it https://github.com/peterdsharpe/AeroSandbox). Aerosandbox is capable of many more, and this only scratches the surface of its capabilities. 

To run the program, download the contents of this repo and XFoil. This program and XFoil MUST be in the same folder for results, or Python will yell at you. Use VSCode, pycharm, etc., to compile the Python code.

 Usage:
 Add all the requested airfoils in list labeled "airfoils". Input the simulation parameters (Re, Mach, alphas, and sort_by). Run the python program.
 

 Current Known Issues:
 1) In the sequence of inputting the airfoils, typing an invalid airfoil and continuing the program will raise an error.
 2) The logic for the inputs that construct the alpha range (First Alpha, Last Alpha, Alpha Increment) is weird. Might yell at you even if you follow the rules
 3) Currently, the max iterations are set to 1000; this should be plenty but high angles of attack might raise an Index error if some solutions are unconverted. The option to change max iterations will be added in the next version.
 4) Currently, if an Excel file already exists with the requested FileName, data will not be written on that Excel file. So the user must not have the Excel file created before running the program. This will be changed in the next version.
 5) The program runs really well for naca 4 digits, but some airfoils in the UIUC website can be problematic. Check the geometry of airfoils from UIUC database to ensure a smooth XFoil run. 

 Future Improvements:
 1) Toggle viscous/inviscid
 2) Option to change max iterations if uncoverged solutions exist
 3) Option to add flaps to airfoils to optimize for flap hinge moment/forces
 4) Graph polars generated
 5) Give the user the option to repanel an airfoil
 6) Option to optimize for CLmax
 7) Remove airfoils once added
 8) Display the inputted airfoils to check for weird geometry (not all the airfoils in the UIUC database are perfect!!)
 9) Add a properties cell in the resulting excel file that lists all the simulation properties the user requested
 10) Transition to a user-friendly GUI

 Feel free to recommend code changes! Always eager to learn.
 
 Contributors:
 Mithun Krishnan, Noah McAllistor
