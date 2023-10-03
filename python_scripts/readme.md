# FEMM / LTspice Automation for WPT FEM simulations

This folder contains the final scrpit versions and utilities used for generating results and functional data analisys tools for the research of "Wireless Power Transfer Through Low Frequency Ressonating Coils".

Essa pasta contém as versões finais e utilitários usados para conseguir resultados e ferramentas funcionais para análises de dados para a pesquisa "Transmissão de Energia Sem Fio Através de Bobinas Ressonantes em Baixas Frequências".

For doubts and futher information, e-mail me on: <dantepedrosa@gmail.com>!

## Contents

This main file explains the purposes of each of the other files in this folder, including:

- ``cleanup.py`` - A cleanup tool used to clear junk files from current folder, gererated in the simulations.  
[Go to section...](#cleanuppy) | [Open file...](cleanup.py)

- ``efficiency_calculation.py`` - Calculates the efficiency of a sigle FEMM file (*.fem) in the folder it's located and prints on result on terminal.   
[Go to section...](#efficiency_calculationpy) | [Open file...](efficiency_calculation.py)

- ``efficiency_calculation_lib.py`` - A library version of ``efficiency_calculation.py`` to be used by other main scripts.   
[Go to section...](#efficiency_calculation_libpy) | [Open file...](efficiency_calculation_lib.py)

- ``efficiency_v_diameter.py`` - A script for calculating the best combination of wire diameter and number of turns in a coil with a static cross section area that yields in the highest efficiency.  
[Go to section...](#efficiency_v_diameterpy) | [Open file...](efficiency_v_diameter.py)

- ``general_simulations.py`` - The gereral simulations file, used for creating simulations such as efficiency as a function of geometry cacacteristcs (area, lenght, distance and wire diameter) and circuit caracteristcs (current, frequency, wire type and load resistance) in one go.  
[Go to section...](#general_simulationspy) | [Open file...](general_simulations.py)   

&nbsp;

## Internal logic

All files that have simulations consist in 3 steps:

1. Get FEMM geometry parameters:

![image](https://github.com/dantepedrosa/WPT-Automation/assets/58957540/31774467-9c60-4a72-9f5c-b159a769d4df)

2. Send parameters to LTspice's SPICE engine:

![image](https://github.com/dantepedrosa/WPT-Automation/assets/58957540/79161dcb-f91f-42b9-8f6c-772a73601d46)
  
3. Get parameters from LTspice's measurements:
```
.meas VIN RMS V(vs)
.meas VOUT RMS V(vl)
.meas IIN RMS I(IS)
.meas IOUT RMS I(RL)
.meas PIN PARAM VIN*IIN
.meas POUT PARAM VOUT*IOUT
.meas EFF PARAM POUT/PIN
```

This is the core logic and the scripts will always have these functions in the code.

&nbsp;


## [``cleanup.py``](cleanup.py)

A cleanup tool used to clear junk files from current folder, gererated in the simulations. 

FEMM and LTspice creae a lot of junk files, including the simulation files itself. This script was used in cases where you didn't clean during the script. 

It deletes the files based on the filetype.


## [``efficiency_calculation.py``](efficiency_calculation.py)

Calculates the efficiency of a sigle FEMM file (*.fem) in the folder it's located and prints on result on terminal.

This can be used to calculate the efficiency of a specific shape, without iterations.


## [``efficiency_calculation_lib.py``](efficiency_calculation_lib.py)

A library version of ``efficiency_calculation.py`` to be used by other main scripts.

Here, the same code as above was organized to be able to be used by other python scripts.


## [``efficiency_v_diameter.py``](efficiency_v_diameter.py)

A script for calculating the best combination of wire diameter and number of turns in a coil with a static cross section area that yields in the highest efficiency.   

It is an specific type of simulation that has to change multiple parameters, so it couldn't be easily added inside the `general_simulations.py` file.

![Diagram - Diameter vs Current](https://github.com/dantepedrosa/WPT-Automation/assets/58957540/02f27285-8a49-4b67-9a78-c911bb3a4996)

## [``general_simulations.py``](general_simulations.py)

The gereral simulations file, used for creating simulations such as efficiency as a function of geometry cacacteristcs (area, lenght, distance and wire diameter) and circuit caracteristcs (current, frequency, wire type and load resistance) in one go.  

This is the most complete version of the script, where you can choose which type of simulation you want and get an interactive graph with efficiency as a funcion of the altered parameter.

For the simulation to happen, the first, last and step values need to be set beforehand, as well as the other values that it may need, for each simulation. It does all simulations in a row and after it finishes, a window opens such as follows:

![image](https://github.com/dantepedrosa/WPT-Automation/assets/58957540/ee6c147a-be5c-4b09-928c-80f82d48cd21)

