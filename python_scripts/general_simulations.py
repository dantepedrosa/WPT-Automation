# Libraries used 
# Python Standard Libraries
import re
import os
import math
import traceback
# Libraries that should be downloaded
import femm
from PyLTSpice.LTSpiceBatch import LTCommander

# Choose which variable the program will change
# For each variable, the program does a loop changing the variable linearly
# The other variables are maintained static during the sweep
loop_enable = {
    "do_default":   True,
    "do_area":      False,  # Not supported yet
    "do_current":   False,
    "do_diameter":  False,
    "do_distance":  False,  # Not supported yet
    "do_freq":      False,
    "do_lenght":    False,  # Not supported yet
    "do_load":      False,
    "do_windRes":   False    
}

# Changes the area of the magnet pole, by simply exteding the corner
_area = {
    "init":     1,      # Initial area to be tested, in millimeters
    "end":      2,      # Final area to be tested, in millimeters
    "step":     1       # Step used in the loop, in millimeters
}

# Changes the input current
_current = {
    "init":     1,      # Initial current to be tested, in Amperes
    "end":      2,      # Final current to be tested, in Amperes
    "step":     1,      # Step used in the loop, in millimeters
    "static":   1       # Static value for current, if "do_current": False
}

# Changes the wire diameter keeping within coil limits (changing turns)
_diameter = {
    "init":     1,      # Initial diameter to be tested, in millimeters
    "end":      2,      # Final diameter to be tested, in millimeters
    "step":     1,      # Step used in the loop, in millimeters
    "lengh":    15,     # Lenght of winding, in millimeters
    "width":    190     # Width of winding, in millimeters
}

# Changes the distance between each coil
_distance = {
    "init":     1,      # Initial distance to be tested, in millimeters
    "end":      2,      # Final distance to be tested, in millimeters
    "step":     1       # Step used in the loop, in millimeters
}

# Changes the frequency of the simulation
_freq = {
    "init":     1,      # Initial frequency to be tested, in Hz
    "end":      2,      # Final frequency to be tested, in Hz
    "step":     1,      # Step used in the loop, in Hz
    "static":   60      # Static value for frequency, if "do_freq": False
}

# Changes the lenght of the shape, horizontally
_lenght = {
    "init":     1,      # Initial lenght to be tested, in millimeters
    "end":      2,      # Final lenght to be tested, in millimeters
    "step":     1       # Step used in the loop, in millimeters
}

# Changes the load resistance (see "create_cir_file" to change load type)
_load = {
    "init":     1,      # Initial load resistance to be tested, in millimeters
    "end":      2,      # Final load resistance to be tested, in millimeters
    "step":     1,      # Step used in the loop, in millimeters
    "static":   146.5   # Static value for load resistance, if "do_load": False
}

# Changes only wire diameter
_windRes = {
    "init":     1,      # Initial wire diameter to be tested, in millimeters
    "end":      2,      # Final wire diameter to be tested, in millimeters
    "step":     1       # Step used in the loop, in millimeters
}

FEMM_filename = ".FEM"  # Keyword to choose FEMM file to analyse 

FEMM_Primary = "Primary"     # The name of the winding to be trated as primary
FEMM_Secondary = "Secondary"  # The name of the winding to be trated as secondary

files_blacklist = []    # List of keywords in files to be deleted.

hide_enable = True        # Set to true if you don't want windows to show


#======================================================================================#
'''=================================================================================='''
#======================================== MAIN ========================================#
'''=================================================================================='''
#======================================================================================#
femm_open = False
def main():

    old_path, new_path, filename = setupFEMM_temp()
    
    femm.openfemm(hide_enable)  # Open FEMM for the first time
    femm_open = True
    
    problem_info = getSettings_FEMM(old_path, filename) # Get orignal problem settings
    
    # Mudar a fonte para corrente ou nããããão ******************************
    # definir como plotar
    
    if loop_enable["do_default"]:
        
        print('\nRunning script for: "do_default"')
        path = "{}\\do_default".format(new_path)
        femm_filepath = "{}\\do_default - {}".format(path, filename)
        
        femm.opendocument(femm_filepath)

        FEMM_Values = getFEMMvalues(_freq["static"], _current["static"], problem_info)
        
        femm.mi_close()
        
        create_cir_file(180, _freq["static"], _load["static"], FEMM_Values, path)
        efficiency = run_LTSpice_sim(path)
        print_eff = round(efficiency*100, 3)
        
        print("\n*************************************************")
        print("The default efficiency of the circuit is {} %".format(print_eff))
        print("*************************************************\n")
   
    
    if loop_enable["do_area"]:
        
        
        print('\nRunning script for: "do_default"')
        path = "{}\\do_area".format(new_path)
        femm_filepath = "{}\\do_area - {}".format(path, filename)
        
        pass


    if loop_enable["do_current"]:
    
        print('\nRunning script for: "do_default"')
        path = "{}\\do_current".format(new_path)
        femm_filepath = "{}\\do_current - {}".format(path, filename)
        
        femm.opendocument(femm_filepath)
        
        x_current = []
        y_current = []
        
        current = _current["init"]
        while (current <= _current["end"]):
        
            FEMM_Values = getFEMMvalues(_freq["static"], current, problem_info)
            create_cir_file(180, _freq["static"], _load["static"], FEMM_Values, path)
            efficiency = run_LTSpice_sim(path)
            
            x_current.append(current)
            y_current.append(efficiency)
            
            current += _current["step"]


    if loop_enable["do_diameter"]:    
        
        print('\nRunning script for: "do_default"')
        path = "{}\\do_diameter".format(new_path)
        femm_filepath = "{}\\do_diameter - {}".format(path, filename)
        pass

  
    if loop_enable["do_distance"]:
    
        print('\nRunning script for: "do_default"')
        path = "{}\\do_distance".format(new_path)
        femm_filepath = "{}\\do_distance - {}".format(path, filename)
        pass


    if loop_enable["do_freq"]:
    
        print('\nRunning script for: "do_default"')
        path = "{}\\do_freq".format(new_path)
        femm_filepath = "{}\\do_freq - {}".format(path, filename)
        
        femm.opendocument(femm_filepath)
        
        x_freq = []
        y_freq = []
        
        freq = _freq["init"]
        while (freq <= _freq["end"]):
        
            FEMM_Values = getFEMMvalues(freq, _current["static"], problem_info)
            create_cir_file(180, freq, _load["static"], FEMM_Values, path)
            efficiency = run_LTSpice_sim(path)
            
            x_freq.append(freq)
            y_freq.append(efficiency)
            
            freq += _freq["step"]


    if loop_enable["do_lenght"]:
        
        print('\nRunning script for: "do_default"')
        path = "{}\\do_lenght".format(new_path)
        femm_filepath = "{}\\do_lenght - {}".format(path, filename)
        pass


    if loop_enable["do_load"]:
    
        print('\nRunning script for: "do_default"')
        path = "{}\\do_load".format(new_path)
        femm_filepath = "{}\\do_load - {}".format(path, filename)
        
        femm.opendocument(femm_filepath)
        
        x_load = []
        y_load = []
        
        FEMM_Values = getFEMMvalues(_freq["static"], _current["static"], problem_info)
        
        load = _load["init"]
        while (load <= _load["end"]):
            
            create_cir_file(180, _freq["static"], load, FEMM_Values, path)
            efficiency = run_LTSpice_sim(path)
            
            x_load.append(load)
            y_load.append(efficiency)
            
            load += _load["step"]

 
    if loop_enable["do_windRes"]:
    
        print('\nRunning script for: "do_default"')
        path = "{}\\do_windRes".format(new_path)
        femm_filepath = "{}\\do_windRes - {}".format(path, filename)
        pass


    femm.closefemm()
    femm_open = False

#======================================================================================#
'''=================================================================================='''
#================================== PROGRAM FUNCTIONS =================================#
'''=================================================================================='''
#======================================================================================#

'''-------------------------------------------------------------------------------------
Name:           setupFEMM_temp
Description:    Detects file to use, and creates a folder to store and run simulations
Input:          -
Output          (string) newpath, temp_file, dir_path, source_file
Ps.:            The name of the file should be defined in "FEMM_filename"
-               If left as "", it will use the firts .FEM file
-------------------------------------------------------------------------------------'''
def setupFEMM_temp(): 

    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    fileFound = False       # Variable used to check error
    
    if FEMM_filename == "":
        fileKey = ".FEM"
    else:
        fileKey = FEMM_filename
        
    for filename in os.listdir(dir_path):
        if ".FEM" in filename:
            if fileKey in filename:
                fileFound = True
                source_file = filename
                print("FEMM file found: " + filename)
                break
            
    # It raises error if file not found
    if not fileFound:
        raise Exception('File not found or name not defined. See "FEMM_filename"')
    
    
    # This creates a new folder, to not fill up original directory with files

    new_path = "{}\\Simulation Files".format(dir_path)
    i = 1
    # Checks whether it already exists a folder, and changes it's name
    while os.path.exists(new_path):
        new_path = "{}\\Simulation Files {}".format(dir_path, i)
        i += 1
        if i > 10:
            raise Exception('Too many "Simulation Files" in directory. '+\
                            'Clean up or change directory')
    os.makedirs(new_path)
    print('\nCreated "Simulation Files {}" folder\n'.format(i))
    
    # Create a copy of the original for each loop
    for key in loop_enable:

        if loop_enable[key]:
        
            loop_path = "{}\\{}".format(new_path, key)  
            os.makedirs(loop_path)
            temp_file = "{}\\{} - {}".format(loop_path, key, source_file)
            os.popen('copy "{}\\{}" "{}"'.format(dir_path, source_file, temp_file))
            print('Created "{}" folder'.format(key))
    
    print()
    
    return dir_path, new_path, source_file 


'''-------------------------------------------------------------------------------------
Name:           init_FEMM
Description:    -
Input:          (string)temp_path       path of file created by getFEMMpath()
                (string)temp_filename   name of file created by getFEMMpath()
                (string)source_path     path of original file from getFEMMpath()
                (string)source_file     name of original file from getFEMMpath()
Output          prob_info[0]            problem type ('axi' or 'planar')
                prob_info[1]            frequency in Hz
                prob_info[2]            problem depth (in the problem unit)
                prob_info[3]            problem unit ('millimeters', 'centimeters'...)
Obs.:           FEMM should already be opened (with femm.openfemm())
-------------------------------------------------------------------------------------'''
def getSettings_FEMM(path, filename):
    
    # Get original problem values
    femm.opendocument("{}\\{}".format(path, filename))
    
    print("Getting original parameters and settings...")
    femm.mi_analyze(hide_enable)
    femm.mi_loadsolution()
    
    prob_info = convertUnits(femm.mo_getprobleminfo())
    
    
    '''
    prob_info content:
    prob_info[0]: problem type ('axi' or 'planar')
    prob_info[1]: frequency in Hz
    prob_info[2]: problem depth (in the problem unit)
    prob_info[3]: problem unit (millimeters, centimeters...)
    '''
    
    # Close original file
    femm.mo_close()
    femm.mi_close()
    print("Succesfully retrieved original parameters and settings")
    
    return prob_info


'''-------------------------------------------------------------------------------------
Name:           getFEMMvalues
Description:    This function FEMM simulation design and returns its values
Input:          (int)                   frequency
                (int)                   current
                (list[4])               problemInfo
Output          FEMM_values_temp[0]     Primary winding resistance
                FEMM_values_temp[1]     Secondary winding resistance
                FEMM_values_temp[2]     Core resistance
                FEMM_values_temp[3]     Primary leakage inductance
                FEMM_values_temp[4]     Secondary leakage inductance
                FEMM_values_temp[5]     Mutual inductance
Obs.:           FEMM should be already opened, and should be closed after it
-------------------------------------------------------------------------------------'''
def getFEMMvalues(freq, current, problemInfo):

    print("\nGetting circuit parameters via FEMM")
    
    # Generic problem definition
    femm.mi_probdef(freq, problemInfo[3], problemInfo[0], 1E-8, problemInfo[2], 30, (0))
    
    # ----------------------------------------------------
    # First simulation - Getting primary and mutual values
    femm.mi_setcurrent(FEMM_Primary, current)
    femm.mi_setcurrent(FEMM_Secondary, 0)
    femm.mi_analyze(hide_enable)
    femm.mi_loadsolution()
    
    primary_props = femm.mo_getcircuitproperties(FEMM_Primary)
    secondary_props = femm.mo_getcircuitproperties(FEMM_Secondary)
    
    # Mutual parameters
    Lm = abs(secondary_props[2].real)/current       # Mutual inductance
    Rc = (abs(primary_props[2].imag)/current)* 2 * math.pi * freq   # Core Resistance
    
    # Primary only parameters
    L1 = (abs(primary_props[2].real)/current) - Lm  # Primary leakage inductance
    R1 = (abs(primary_props[1].real)/current) - Rc  # Primary winding resistance
    
    femm.mo_close()
    
    # --------------------------------------------
    # Second simulation - Getting secondary values
    femm.mi_setcurrent(FEMM_Primary, 0)
    femm.mi_setcurrent(FEMM_Secondary, current)
    femm.mi_analyze(hide_enable)
    femm.mi_loadsolution()
    
    secondary_props = femm.mo_getcircuitproperties(FEMM_Secondary)
    
    # Secondary only parameters
    L2 = (abs(secondary_props[2].real)/current) - Lm    # Secondary leakage inductance
    R2 = (abs(secondary_props[1].real)/current) - Rc    # Secondary winding resistance
    
    femm.mo_close()
    
    FEMM_values_temp = [R1, R2, Rc, L1, L2, Lm]
    
    print("FEMM simulation was successful")

    return FEMM_values_temp


'''-------------------------------------------------------------------------------------
Name:           create_net_file
Description:    Creates a LTSpice netlist file of the equivalent circuit
Input:          var         V_source    Voltage source in V
                var         freq        Frequency in Hz
                var         RL          Load resistance in Ohms
                array[6]    R1 to Lm    Values described in getFEMMvalues()
                string      path        
Output          -
-------------------------------------------------------------------------------------'''
def create_cir_file(V_source, freq, RL, FEMM_values, path):
    
    # To facilitate understanding of the function
    R1 = FEMM_values[0]
    R2 = FEMM_values[1]
    Rc = FEMM_values[2]
    L1 = FEMM_values[3]
    L2 = FEMM_values[4]
    Lm = FEMM_values[5]
    
    # Calculation of extra parameters: C1 and C2
    X1 = L1 * 2 * math.pi * freq
    X2 = L2 * 2 * math.pi * freq
    Xm = Lm * 2 * math.pi * freq
    
    C1 = ((X1+Xm)* 2 * math.pi * freq)**(-1)
    C2 = ((((Xm / (Xm + X2))**2 * RL)**2 / ((Xm*X1 + X1*X2 + X2*Xm)/(Xm+X2)) + \
         ((Xm*X1 + X1*X2 + X2*Xm)/(Xm+X2)))* 2 * math.pi * freq)**(-1)

    # To ease access to components
    FEMM_values.append(C1)
    FEMM_values.append(C2)
    FEMM_values.append(RL)
    FEMM_values.append(V_source)
    FEMM_values.append(freq)
         
    period_T    = 1/freq
    time_step   = period_T * 0.0001
    stop_time   = period_T * 100
    start_time  = period_T * 10
    
    print("\nCreating .cir file")
    
    cirFile = open("{}\\Equivalent_Circuit.cir".format(path), "w")

    cirFile.write("WPT Equivalent Circuit Efficiency Calculation\n")
    cirFile.write("V1 Vs 0 SINE(0 {} {} 0 0 0)\n".format(V_source, freq))
    cirFile.write("RL Vl 0 {}\n".format(RL))
    cirFile.write("C1 Vs 0 {}\n".format(C1))
    cirFile.write("R1 N001 Vs {}\n".format(R1))
    cirFile.write("L1 N001 N002 {}\n".format(L1))

    cirFile.write("C2 Vl 0 {}\n".format(C2))
    cirFile.write("R2 N003 N002 {}\n".format(R2))
    cirFile.write("L2 N003 Vl {}\n".format(L2))

    cirFile.write("Lm N004 0 {}\n".format(Lm))
    cirFile.write("Rc N002 N004 {}\n".format(Rc))
    
    cirFile.write(".tran 0 {} {} {}\n".format(stop_time, start_time, time_step))
    cirFile.write(".meas VIN RMS V(vs)\n")
    cirFile.write(".meas VOUT RMS V(vl)\n")
    cirFile.write(".meas IIN RMS I(V1)\n")
    cirFile.write(".meas IOUT RMS I(RL)\n")
    cirFile.write(".meas PIN PARAM VIN*IIN\n")
    cirFile.write(".meas POUT PARAM VOUT*IOUT\n")
    cirFile.write(".meas ZIN PARAM VIN/IIN\n")
    cirFile.write(".meas EFF PARAM POUT/PIN\n")
    cirFile.write(".end\n")

    cirFile.close()
    print("Succesfully created .cir file")
    
    '''
    print("\nCreated Equivalent_Circuit.cir file")
    print("Values used for equivalent circuit:\n")
    print("V1 = {} V, {} Hz".format(V_source, freq))
    print("RL = {} Ω".format(RL))
    print("R1 = {} Ω".format(R1))
    print("R2 = {} Ω".format(R2))
    print("Rc = {} Ω".format(Rc))
    print("L1 = {} H".format(L1))
    print("L2 = {} H".format(L2))
    print("Lm = {} H".format(Lm))
    print("C1 = {} F".format(C1))
    print("C2 = {} F".format(C2))
    '''


'''-------------------------------------------------------------------------------------
Name:           run_LTSpice_sim
Description:    Runs LTSpice simulation using PyLTSpice, and returns the efficiency
Input:          (str)   path
Output          efficiency (decimal form)
-------------------------------------------------------------------------------------'''
def run_LTSpice_sim(path):

    print("\nRunning LTSPice simulation")
    
    LTC = LTCommander(path + "\\Equivalent_Circuit.cir")
    rawfile, logfile = LTC.run()
    LTC.wait_completion()
    
    with open(logfile) as fd:

        # Iterate over the lines
        for line in fd:
            # Capture one-or-more characters of non-whitespace after the initial match
            match = re.search(r'eff: pout/pin=(\S+)', line)
            # Did we find a match?
            if match:
                # Yes, process it
                efficiency = float(match.group(1))
    
    print("LTSPice simulation was successfull")
    
    return efficiency


'''-------------------------------------------------------------------------------------
Name:           convertUnits
Description:    Converts the information outputed by FEMM to the proper input form
Input:          (array[4])problem_info
Output          (array[4])problem_info
Obs.:           The parameters of the first four are descriped in "init_FEMM()"
-------------------------------------------------------------------------------------'''
def convertUnits(problem_info):
    
    # Convert problem type to text
    if problem_info[0]:
        problem_info[0] = 'axi'
    else:
        problem_info[0] = 'planar'
    
    # Convert problem depth (from meters to chosen unit)
    problem_info[2] *= problem_info[3]**-1
    
    # Convert units to text
    if problem_info[3] == 1:
        problem_info[3] = "meters"
    elif problem_info[3] == 0.01:
        problem_info[3] = "centimeters"
    elif problem_info[3] == 0.001:
        problem_info[3] = "millimeters"
    else:
        raise Exception("The unit defined in the FEMM file is not suppoted\n" + \
                        "Use either 'Meters', 'Centimeters' or 'Millimeters'")
        
    return problem_info


'''-------------------------------------------------------------------------------------
Name:           cleanFolder
Description:    Deletes files in folder that the script is located. Should be one of the
_               last functions to be called
Input:          -
Output          -
Ps.:            Any file with any of the keywords in "files_blacklist" will be deleted
-------------------------------------------------------------------------------------'''
def cleanFolder():
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    count = 0
    for filename in os.listdir(dir_path):
    
        for keyword in files_blacklist:
        
            if keyword in filename:
                os.remove(filename)
                print("\nDeleted {}".format(filename))
                count += 1
            
    print("\nDeleted {} files in total\n".format(count))


'''-------------------------------------------------------------------------------------
Name:           after_ERROR
Description:    -
Input:          -
Output          -
-------------------------------------------------------------------------------------'''
def handle_ERROR():
    if femm_open:
        femm.closefemm()
    print("↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑")
    print("An error ocurred.  (ノಠ益ಠ)ノ彡┻┻   FEMM closed.")
    

#======================================================================================#
'''=================================================================================='''
#=================================== ACTUAL PROGRAM ===================================#
'''=================================================================================='''
#======================================================================================#

try:
    main()
except Exception:
    print(traceback.format_exc())
    handle_ERROR()
except KeyboardInterrupt:
    print()
    print(traceback.format_exc())
    handle_ERROR()
else:
    print("---------------------------------------------------\n"+\
          "Simulation was successful!!  ♪┏(・o･)┛ ♪ ┗( ･o･)┓"+\
          "\n---------------------------------------------------")
finally:
    print("\nType anything and press enter to exit script")
    input()