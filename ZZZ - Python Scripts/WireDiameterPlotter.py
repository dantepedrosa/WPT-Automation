import math
import femm
import Efficiency_Calculation_Final_LIB

import os

from PyLTSpice.LTSpiceBatch import LTCommander
import re

# Measure diameters
comprimento = 220      # In millimeters
largura = 2.5          # In millimeters
initialDiameter = 5    # In one tenth of a millimeter
finalDiameter = 25     # In one tenth of a millimeter

#Primary blocks coordinates
x1_1, y1_1 = -0.02, 6.38    # Positive turns
x1_2, y1_2 = 3, 7.6         # Negative turns

#Secondary blocks coordinates
x2_1, y2_1 = 2.38, 13.61   # Positive turns
x2_2, y2_2 = -0.2, 12.3    # Negative turns


def change_turns(n_ofTurns, diameter):
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for filename in os.listdir(dir_path):
        if ".FEM" in filename:
            break
    if ".FEM" not in filename:
        errorWarning = 2/0
    
    femm.openfemm(1)
    femm.opendocument(dir_path + '\\' + filename)
    
    femm.mi_addmaterial(('Copper Wire '+ str(diameter/10)) , 1, 1, 0, 0, 58, 0, 0, 1, 3, 0, 0, 1, diameter/10)
    
    femm.mi_selectlabel(x1_1, y1_1)
    femm.mi_setblockprop(('Copper Wire '+ str(diameter/10)), 1, 0, 'Primary', 0, 0, n_ofTurns)
    femm.mi_clearselected()
    
    femm.mi_selectlabel(x1_2, y1_2)
    femm.mi_setblockprop(('Copper Wire '+ str(diameter/10)), 1, 0, 'Primary', 0, 0, (n_ofTurns * -1))
    femm.mi_clearselected()
    
    femm.mi_selectlabel(x2_1, y2_1)
    femm.mi_setblockprop(('Copper Wire '+ str(diameter/10)), 1, 0, 'Secondary', 0, 0, n_ofTurns)
    femm.mi_clearselected()
    
    femm.mi_selectlabel(x2_2, y2_2)
    femm.mi_setblockprop(('Copper Wire '+ str(diameter/10)), 1, 0, 'Secondary', 0, 0, (n_ofTurns * -1))
    femm.mi_clearselected()
    
    femm.mi_saveas(filename)
    femm.closefemm()

def cleanFolder():
    
    blacklist = [".raw", ".masterlog", "LTSpiceBatch", ".net"]
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    deletedFiles = 0
    
    for filename in os.listdir(dir_path):
        for fileString in blacklist:
        
            if fileString in filename:
                os.remove(filename)
                deletedFiles += 1
            
    print("Deleted " + str(deletedFiles) + " files")

#--------------------------------- MAIN ---------------------------------
file = open(("GraphPlotText.csv"), "w")

for diameter in range(initialDiameter, (finalDiameter+1), 2):
    
    colunas = math.trunc( largura / (diameter/10) )
    linhas = math.trunc( comprimento / (diameter/10) )
    voltas = math.trunc(linhas * colunas * 0.8)
    change_turns(voltas, diameter)
    
    properties, efficiency, capacitance = Efficiency_Calculation_Final_LIB.main()
    
    file.write(str(diameter/10) + ',' + str(voltas) + ',' + str(properties[0]) + ',' + str(properties[2]) + ',' + str(capacitance) + ',' + str(efficiency) + '\n')
    print(diameter/10)
    print(voltas)
    

    #print(properties)
    #print(efficiency)
file.close()

cleanFolder()

#exec(open('Efficiency Calculation_Final').read())
