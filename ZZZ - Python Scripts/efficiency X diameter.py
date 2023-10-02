import math
import femm
import Efficiency_Calculation_Final_LIB

import os

from PyLTSpice.LTSpiceBatch import LTCommander
import re

# Measure diameters
comprimento = 198      # In millimeters
largura = 10           # In millimeters
initialDiameter = 5    # In one tenth of a millimeter
finalDiameter = 30     # In one tenth of a millimeter

#Primary blocks coordinates
x1_1, y1_1 = 4, 131    # Positive turns
x1_2, y1_2 = 1, 66     # Negative turns

#Secondary blocks coordinates
x2_1, y2_1 = 1, -132   # Positive turns
x2_2, y2_2 = 2, -70    # Negative turns


def change_turns(n_ofTurns, diameter):
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for filename in os.listdir(dir_path):
        if ".FEM" in filename:
            break
    if ".FEM" not in filename:
        x = 2/0
    
    femm.openfemm()
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
    i = 0
    
    for filename in os.listdir(dir_path):
        for fileString in blacklist:
        
            if fileString in filename:
                os.remove(filename)
                i++
            
    print("Deleted " + str(i) + " files")

#--------------------------------- MAIN ---------------------------------
file = open(("GraphPlotText.txt"), "w")

for i in range(initialDiameter, (finalDiamter+1)):
    
    colunas = math.trunc( largura / (i/10) )
    linhas = math.trunc( comprimento / (i/10) )
    voltas = math.trunc(linhas * colunas * 0.8)
    change_turns(voltas, i)
    
    properties, efficiency, capacitance = Efficiency_Calculation_Final.main()
    
    file.write(str(i/10) + ',' + str(voltas) + ',' + str(properties[0]) + ',' + str(properties[2]) + ',' + str(capacitance) + ',' + str(efficiency) + '\n')
    print(i/10)
    print(voltas)
    

    #print(properties)
    #print(efficiency)
file.close()

cleanFolder()

#exec(open('Efficiency Calculation_Final').read())
