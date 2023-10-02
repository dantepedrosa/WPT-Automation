import os
import femm

from PyLTSpice.LTSpiceBatch import LTCommander
import re


def FEMM_results(path, femmfile):

    # Open document ----------------------------------------------
    femm.openfemm(1)
    femm.opendocument(path + '\\' + femmfile)

    # Get original values ----------------------------------------
    femm.mi_analyze(1)
    femm.mi_loadsolution()
    probleminfo = femm.mo_getprobleminfo()
    changedProbInfo = [None, None, None, None]
    changedProbInfo[1] = probleminfo[1]
    changedProbInfo[3], changedProbInfo[2], changedProbInfo[0] = checkunity(probleminfo[3], probleminfo[2], probleminfo[0])
    
    primaryProps = femm.mo_getcircuitproperties("Primary")
    secondaryProps = femm.mo_getcircuitproperties("Secondary")

    primaryCurrent = primaryProps[0]
    secondaryCurrent = secondaryProps[0]
    femm.mo_close()

    # Get non-frequency dependent values ------------------------
    # Primary and Secondary Inductance and Resistance, and mutual inductance
    femm.mi_probdef(0, changedProbInfo[3], changedProbInfo[0], 1E-8, changedProbInfo[2], 30, (0))
    femm.mi_setcurrent("Primary", 1)
    femm.mi_setcurrent("Secondary", 0)
    femm.mi_analyze(1)

    femm.mi_loadsolution()
    primaryProps = femm.mo_getcircuitproperties("Primary")
    primaryInductance = abs(primaryProps[2])
    primaryResistance = abs(primaryProps[1])
    secondaryProps = femm.mo_getcircuitproperties("Secondary")
    mutualInductance = abs(secondaryProps[2])
    femm.mo_close()

    femm.mi_setcurrent("Primary", 0)
    femm.mi_setcurrent("Secondary", 1)
    femm.mi_analyze(1)

    femm.mi_loadsolution()
    secondaryProps = femm.mo_getcircuitproperties("Secondary")
    secondaryInductance = abs(secondaryProps[2])
    secondaryResistance = abs(secondaryProps[1])
    femm.mo_close()

    # Value for 60 Hz --------------------------------------------
    # Core Resistance
    femm.mi_probdef(60, changedProbInfo[3], changedProbInfo[0], 1E-8, changedProbInfo[2], 30, (0))
    femm.mi_setcurrent("Primary", 1)
    femm.mi_setcurrent("Secondary", 0)
    femm.mi_analyze(1)

    femm.mi_loadsolution()
    primaryProps = femm.mo_getcircuitproperties("Primary")
    coreResistance = abs(primaryProps[2].imag) * 2 * 60 * 3.1415926
    femm.mo_close()
    
    # Return to original values

    femm.mi_probdef(probleminfo[1], changedProbInfo[3], changedProbInfo[0], 1E-8, changedProbInfo[2], 30, (0))
    femm.mi_setcurrent("Primary", primaryCurrent)
    femm.mi_setcurrent("Secondary", secondaryCurrent)
    
    femm.closefemm()
    
    # Returns a tuple in following order
    # 0 - Prim. Inductance  |   3 - Sec. Resistance
    # 1 - Sec.  Inductance  |   4 - Mut. Inductance
    # 2 - Prim. Resistance  |   5 - Core Resistance
    return [primaryInductance, secondaryInductance, primaryResistance, secondaryResistance, mutualInductance, coreResistance]

'''
Function: checkunity()
Receives raw output from FEMM's "mo_getprobleminfo()" and transforms into usable "mi_probdef()" input
    Input:  problemUnity (int), problemDepth (int), problemtype(int)
    Output: unity (str),        depth (int),        type(str)
'''
def checkunity(problemUnity, problemDepth, problemType):

    unity = ""
    lenght = problemDepth
    if problemType:
        probType = 'axi'
    else:
        probType = 'planar'
    
    if problemUnity == 1:
        unity = "meters"
    elif problemUnity == 0.01:
        unity = "centimeters"
    elif problemUnity == 0.001:
        unity = "millimeters"
    
    if unity == "meters":
        return 'meters', lenght, probType
    elif unity == "centimeters":
        return 'centimeters', (lenght * 100), probType
    elif unity == "millimeters":
        return 'millimeters', (lenght * 1000), probType

'''
Function: getCircuitProps()
Detects either FEMM or CST file and gets properties such as:

    0 - Prim. Inductance  |   3 - Sec. Resistance
    1 - Sec.  Inductance  |   4 - Mut. Inductance
    2 - Prim. Resistance  |   5 - Core Resistance

Obs.: The Inductance is given as self, not leakage inductance

    Input:  -
    Output: circuitProps[6]
'''
def getCircuitProps(): 

    dir_path = os.path.dirname(os.path.realpath(__file__))

    for filename in os.listdir(dir_path):

        if ".FEM" in filename:
            print("Running FEMM equivalent circuit...")
            circuitProperties = FEMM_results(dir_path, filename)
            break

    #     if "CST.txt" in filename:
    #         print("Running CST equivalent circuit...")
    #         CST_results(filename)
    # 
    #         break

    return circuitProperties


#----------------------------------------------------------------------------------------------------
def get_efficiency(parameterList):

    # Parameters definition

    primary_leakage = (parameterList[0]-parameterList[4])
    primary_res = parameterList[2]
    secondary_leakage = (parameterList[1]-parameterList[4])
    secondary_res = parameterList[3]
    mutual_ind = parameterList[4]
    core_res = parameterList[5]
    primary_capacitance = ((((mutual_ind * secondary_leakage)/(mutual_ind + secondary_leakage)) + primary_leakage)*142122.30)**-1
    secondary_capacitance = ((((mutual_ind * primary_leakage)/(mutual_ind + primary_leakage)) + secondary_leakage)*142122.30)**-1
    load_res = 10
    
    kcoefficient = (parameterList[4]/parameterList[0])
    
    f = open("Equivalent_Circuit.cir", "w")

    f.write("Equivalent Circuit Efficiency Calculation\n")
    f.write("Vcc Vs 0 SINE(0 180 60 0 0 0)\n")
    f.write("Rl Vl 0 " + str(load_res) + "\n")

    f.write("C1 Vs 0 " + str(primary_capacitance) + "\n")
    f.write("R1 N001 Vs " + str(primary_res) + "\n")
    f.write("L1 N001 N002 " + str(primary_leakage) + "\n")

    f.write("C2 Vl 0 " + str(secondary_capacitance) + "\n")
    f.write("R2 N003 N002 " + str(secondary_res) + "\n")
    f.write("L2 N003 Vl " + str(secondary_leakage) + "\n")

    f.write("Lm N004 0 " + str(mutual_ind) + "\n")
    f.write("Rc N002 N004 " + str(core_res) + "\n")

    f.write(".tran 0 1666.667m 166.667m 166.66667u\n")
    f.write(".meas VIN RMS V(vs)\n")
    f.write(".meas VOUT RMS V(vl)\n")
    f.write(".meas IIN RMS I(Vcc)\n")
    f.write(".meas IOUT RMS I(rl)\n")
    f.write(".meas PIN PARAM VIN*IIN\n")
    f.write(".meas POUT PARAM VOUT*IOUT\n")
    f.write(".meas EFF PARAM POUT/PIN\n")
    f.write(".end\n")

    f.close()
    
    #Run LTSpice netlist and get efficiency from logfile
    
    meAbsPath = os.path.dirname(os.path.realpath(__file__))

    LTC = LTCommander(meAbsPath + "\\Equivalent_Circuit.cir")
    rawfile, logfile = LTC.run()
    LTC.wait_completion()

    print("Prim. Leakage:     " + str(round(primary_leakage, 8)) + ' H')
    print("Sec.  Leakage:     " + str(round(secondary_leakage, 8)) + ' H')
    print("Prim. Resistance:  " + str(round(primary_res, 8)) + ' R')
    print("Sec.  Resistance:  " + str(round(secondary_res, 8)) + ' R')
    print("Prim. Capacitance: " + str(round(primary_capacitance, 8)) + ' F')
    print("Sec.  Capacitance: " + str(round(secondary_capacitance, 8)) + ' F')
    print("Mut.  Inductance:  " + str(round(mutual_ind, 8)) + ' H')
    print("Core  Resistance:  " + str(round(core_res, 8)) + ' R')
    print("Load  Resistance:  " + str(round(load_res, 7)) + ' R')
    
    
    # Open the file for reading
    with open(logfile) as fd:

        # Iterate over the lines
        for line in fd:

            # Capture one-or-more characters of non-whitespace after the initial match
            match = re.search(r'eff: pout/pin=(\S+)', line)

            # Did we find a match?
            if match:
                # Yes, process it
                efficiency = match.group(1)
                
                f = open(("Efficiency Calculation Result.txt"), "w")
                f.write("********** The efficiency of the design is " + efficiency + " **********\n")
                f.write("Prim. Leakage:     " + str(round(primary_leakage, 8)) + ' H\n')
                f.write("Sec.  Leakage:     " + str(round(secondary_leakage, 8)) + ' H\n')
                f.write("Prim. Resistance:  " + str(round(primary_res, 8)) + ' R\n')
                f.write("Sec.  Resistance:  " + str(round(secondary_res, 8)) + ' R\n')
                f.write("Prim. Capacitance: " + str(round(primary_capacitance, 8)) + ' F\n')
                f.write("Sec.  Capacitance: " + str(round(secondary_capacitance, 8)) + ' F\n')
                f.write("Mut.  Inductance:  " + str(round(mutual_ind, 8)) + ' H\n')
                f.write("Core  Resistance:  " + str(round(core_res, 8)) + ' R\n')
                f.write("Load  Resistance:  " + str(round(load_res, 7)) + ' R\n')
                f.write("\n")
                f.write('K coefficient is: '+ str(kcoefficient))
                
                return efficiency
            
            
def cleanFolder():
    
    blacklist = [".raw", ".masterlog", "LTSpiceBatch", ".net"]
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    i = 0
    
    for filename in os.listdir(dir_path):
        for fileString in blacklist:
        
            if fileString in filename:
                os.remove(filename)
                i += 1
            
    print("Deleted " + str(i) + " files")
    


# MAIN
circuitProps = getCircuitProps()

circuitEfficiency = get_efficiency(circuitProps)

print("")
print("The efficiency of the circuit is " + circuitEfficiency)
print("\n")
print('K coefficient is: '+ str(circuitProps[4]/circuitProps[0]))

cleanFolder()
