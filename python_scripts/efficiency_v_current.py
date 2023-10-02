import math
import femm
import efficiency_v_current_lib

import matplotlib.pyplot as plt

import os

from PyLTSpice.LTSpiceBatch import LTCommander
import re


initialCurrent = 1      # In Amperes x 10
finalCurrent = 400      # In Amperes x 10

def cleanFolder():
    
    blacklist = [".raw", ".masterlog", ".net", "LTSpiceBatch"]
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    deletedFiles = 0
    
    for filename in os.listdir(dir_path):
        for fileString in blacklist:
        
            if fileString in filename:
                os.remove(filename)
                deletedFiles += 1
            
    print("Deleted " + str(deletedFiles) + " files")

def plotGraph(x, y):
    # plotting the points  
    plt.plot(x, y) 
      
    # naming the x axis 
    plt.xlabel('Measured data') 
    # naming the y axis 
    plt.ylabel('Efficiency') 
      
    # function to show the plot 
    plt.show() 

#--------------------------------- MAIN ---------------------------------
    
try:

    file = open(("GraphPlotText.csv"), "w")
    file.write("Current,Inductance,Resistance,Capacitance,Efficiency\n")

    curData = []
    effData = []

    for current in range(initialCurrent, (finalCurrent+1), 20):
        
        properties, efficiency, capacitance = efficiency_v_current_lib.main(current/10)
        
        curData.append(current/10)
        effData.append(efficiency*100)
        
        file.write(str(current/10) + ',' + str(properties[0]) + ',' + str(properties[2]) + ',' + str(capacitance) + ',' + str(efficiency) + '\n')
        print(current/10)

except KeyboardInterrupt:
    print ('Caught KeyboardInterrupt')
    
finally:
    
    file.close()
    cleanFolder()
    plotGraph(curData, effData)